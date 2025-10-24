from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from middleware.auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/reviews", tags=["reviews"])

async def get_db():
    from server import db
    return db

class ReviewCreate(BaseModel):
    product_id: str
    rating: int
    review: str

class Review(BaseModel):
    id: str
    product_id: str
    user_name: str
    rating: int
    review: str
    created_at: str
    verified_purchase: bool

@router.get("/product/{product_name}")
async def get_product_reviews(
    product_name: str,
    limit: int = Query(10, ge=1, le=50),
    skip: int = Query(0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Decode URL encoded product name
    import urllib.parse
    decoded_product_name = urllib.parse.unquote(product_name)
    
    reviews = await db.reviews.find(
        {"product_id": decoded_product_name},
        {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total = await db.reviews.count_documents({"product_id": decoded_product_name})
    
    # Calculate rating distribution
    ratings_pipeline = [
        {"$match": {"product_id": decoded_product_name}},
        {"$group": {"_id": "$rating", "count": {"$sum": 1}}}
    ]
    rating_dist = await db.reviews.aggregate(ratings_pipeline).to_list(None)
    
    rating_distribution = {str(i): 0 for i in range(1, 6)}
    for item in rating_dist:
        rating_distribution[str(item["_id"])] = item["count"]
    
    return {
        "reviews": reviews,
        "total": total,
        "rating_distribution": rating_distribution
    }

@router.post("")
async def create_review(
    review_data: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if product exists
    product = await db.products.find_one({"name": review_data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already reviewed this product
    existing_review = await db.reviews.find_one({
        "product_id": review_data.product_id,
        "user_id": current_user["user_id"]
    })
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    
    # Get user info
    user = await db.users.find_one({"id": current_user["user_id"]})
    
    review = {
        "id": str(uuid.uuid4()),
        "product_id": review_data.product_id,
        "user_id": current_user["user_id"],
        "user_name": user["name"] if user else "Anonymous",
        "rating": review_data.rating,
        "review": review_data.review,
        "created_at": datetime.utcnow().isoformat(),
        "verified_purchase": True
    }
    
    await db.reviews.insert_one(review)
    
    # Update product rating
    all_reviews = await db.reviews.find({"product_id": review_data.product_id}).to_list(None)
    avg_rating = sum([r["rating"] for r in all_reviews]) / len(all_reviews)
    
    await db.products.update_one(
        {"name": review_data.product_id},
        {"$set": {"rating": round(avg_rating, 1), "reviews": len(all_reviews)}}
    )
    
    return {"review": review, "message": "Review added successfully"}