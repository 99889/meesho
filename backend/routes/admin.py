from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from middleware.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

async def get_db():
    from server import db
    return db

async def verify_admin(current_user = Depends(get_current_user), db = Depends(get_db)):
    # Fetch user from database to check role
    user_data = await db.users.find_one({"id": current_user["user_id"]})
    if not user_data or user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_data

@router.get("/products")
async def get_all_products(
    db = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    """Get all products (admin only)"""
    products = await db.products.find({}, {"_id": 0}).to_list(None)
    total = await db.products.count_documents({})
    
    return {
        "products": products,
        "total": total
    }

@router.delete("/products/{product_id}")
async def admin_delete_product(
    product_id: str,
    db = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    """Delete any product (admin only)"""
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await db.products.delete_one({"id": product_id})
    return {"success": True, "message": "Product deleted by admin"}