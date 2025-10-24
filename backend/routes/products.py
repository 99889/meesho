from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.product import Product, ProductCreate, ProductUpdate
from middleware.auth import get_current_user
from datetime import datetime
import bson
from bson import json_util
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/products", tags=["products"])

async def get_db():
    from server import db
    return db

@router.get("")
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    discount: Optional[float] = None,
    rating: Optional[float] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db = Depends(get_db)
):
    query = {}
    
    if category:
        query["category"] = category
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ]
    
    if discount is not None:
        query["discount"] = {"$gte": discount}
    
    if rating is not None:
        query["rating"] = {"$gte": rating}
    
    if max_price is not None or min_price is not None:
        query["price"] = {}
        if max_price is not None:
            query["price"]["$lte"] = max_price
        if min_price is not None:
            query["price"]["$gte"] = min_price
    
    products = await db.products.find(query, {"_id": 0}).skip(skip).limit(limit).to_list(limit)
    total = await db.products.count_documents(query)
    
    return {
        "products": products,
        "total": total,
        "limit": limit,
        "skip": skip
    }

@router.get("/{product_id}")
async def get_product(product_id: str, db = Depends(get_db)):
    # Try to find by name first (for URL-friendly names), then by id
    product = await db.products.find_one({"name": product_id}, {"_id": 0})
    if not product:
        product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"product": product}

@router.post("")
async def create_product(
    product_data: ProductCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    # Only sellers and admins can create products
    # First check if role is in the token
    user_role = current_user.get("role")
    if not user_role:
        # If role is not in token, fetch user from database to check role
        user_data = await db.users.find_one({"id": current_user["user_id"]})
        if not user_data:
            raise HTTPException(status_code=403, detail="Not authorized to create products")
        user_role = user_data.get("role")
    
    if user_role not in ["seller", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create products")
    
    # Prepare product data, ensuring we don't pass seller_name twice
    product_dict = product_data.dict()
    # Remove seller_name from product_dict if it exists to avoid duplication
    product_dict.pop("seller_name", None)
    
    product = Product(
        **product_dict,
        seller_id=current_user["user_id"],
        seller_name=current_user.get("name", "Unknown Seller")  # Auto-fill seller name
    )
    
    # Convert datetime objects to strings for proper JSON serialization
    product_dict = product.dict()
    if "created_at" in product_dict:
        product_dict["created_at"] = product_dict["created_at"].isoformat()
    if "updated_at" in product_dict:
        product_dict["updated_at"] = product_dict["updated_at"].isoformat()
    
    await db.products.insert_one(product_dict)
    
    # Remove MongoDB's _id field if it exists
    if "_id" in product_dict:
        del product_dict["_id"]
    
    return {"product": product_dict}

@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user is the seller or admin
    # First check if role is in the token
    user_role = current_user.get("role")
    if not user_role:
        # If role is not in token, fetch user from database to check role
        user_data = await db.users.find_one({"id": current_user["user_id"]})
        if not user_data:
            raise HTTPException(status_code=403, detail="Not authorized")
        user_role = user_data.get("role")
    
    if user_role != "admin" and product.get("seller_id") != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {k: v for k, v in product_data.dict().items() if v is not None}
    
    if update_data:
        # Update the updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        await db.products.update_one({"id": product_id}, {"$set": update_data})
    
    # Fetch the updated product and exclude MongoDB's _id field
    updated_product = await db.products.find_one({"id": product_id}, {"_id": 0})
    
    # Convert datetime objects to strings for proper JSON serialization
    if updated_product and "created_at" in updated_product:
        updated_product["created_at"] = updated_product["created_at"].isoformat()
    if updated_product and "updated_at" in updated_product:
        updated_product["updated_at"] = updated_product["updated_at"].isoformat()
    
    return {"product": updated_product}

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user is the seller or admin
    # First check if role is in the token
    user_role = current_user.get("role")
    if not user_role:
        # If role is not in token, fetch user from database to check role
        user_data = await db.users.find_one({"id": current_user["user_id"]})
        if not user_data:
            raise HTTPException(status_code=403, detail="Not authorized")
        user_role = user_data.get("role")
    
    if user_role != "admin" and product.get("seller_id") != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.products.delete_one({"id": product_id})
    return {"success": True, "message": "Product deleted"}