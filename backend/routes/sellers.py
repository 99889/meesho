from fastapi import APIRouter, HTTPException, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.seller import SellerProfile, SellerProfileCreate, SellerProfileUpdate, SellerReview, SellerReviewCreate, SellerReviewResponse, SellerProfileResponse
from middleware.auth import get_current_user
from typing import List

router = APIRouter(prefix="/sellers", tags=["sellers"])

async def get_db():
    from server import db
    return db

@router.post("/profile", response_model=SellerProfileResponse)
async def create_seller_profile(
    profile: SellerProfileCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a seller profile for the current user"""
    # Check if seller profile already exists
    existing = await db.sellers.find_one({"user_id": current_user["id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Seller profile already exists")
    
    new_profile = SellerProfile(
        user_id=current_user["id"],
        **profile.dict()
    )
    
    result = await db.sellers.insert_one(new_profile.dict())
    new_profile.id = str(result.inserted_id)
    return new_profile

@router.get("/profile/{seller_id}", response_model=SellerProfileResponse)
async def get_seller_profile(
    seller_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get seller profile by seller ID"""
    profile = await db.sellers.find_one(
        {"id": seller_id},
        {"_id": 0}
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Seller not found")
    return profile

@router.get("/user/{user_id}", response_model=SellerProfileResponse)
async def get_seller_by_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get seller profile by user ID"""
    profile = await db.sellers.find_one(
        {"user_id": user_id},
        {"_id": 0}
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Seller profile not found")
    return profile

@router.get("/my-profile")
async def get_my_seller_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get current user's seller profile"""
    profile = await db.sellers.find_one(
        {"user_id": current_user["id"]},
        {"_id": 0}
    )
    if not profile:
        raise HTTPException(status_code=404, detail="You don't have a seller profile")
    return profile

@router.put("/profile/{seller_id}", response_model=SellerProfileResponse)
async def update_seller_profile(
    seller_id: str,
    profile_update: SellerProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update seller profile"""
    # Verify ownership
    seller = await db.sellers.find_one({"id": seller_id})
    if not seller or seller["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    update_data = {k: v for k, v in profile_update.dict().items() if v is not None}
    
    result = await db.sellers.update_one(
        {"id": seller_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    updated_profile = await db.sellers.find_one(
        {"id": seller_id},
        {"_id": 0}
    )
    return updated_profile

@router.post("/reviews", response_model=SellerReviewResponse)
async def create_seller_review(
    review: SellerReviewCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a review for a seller"""
    # Verify order exists and user is the buyer
    order = await db.orders.find_one({"id": review.order_id})
    if not order or order["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to review this seller")
    
    new_review = SellerReview(
        user_id=current_user["id"],
        **review.dict()
    )
    
    result = await db.seller_reviews.insert_one(new_review.dict())
    new_review.id = str(result.inserted_id)
    
    # Update seller rating
    reviews = await db.seller_reviews.find(
        {"seller_id": review.seller_id},
        {"_id": 0}
    ).to_list(None)
    
    if reviews:
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
        await db.sellers.update_one(
            {"id": review.seller_id},
            {"$set": {"rating": avg_rating, "total_reviews": len(reviews)}}
        )
    
    return new_review

@router.get("/reviews/{seller_id}", response_model=List[SellerReviewResponse])
async def get_seller_reviews(
    seller_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Get reviews for a seller"""
    reviews = await db.seller_reviews.find(
        {"seller_id": seller_id},
        {"_id": 0}
    ).skip(skip).limit(limit).to_list(limit)
    return reviews

@router.get("", response_model=List[SellerProfileResponse])
async def get_all_sellers(
    db: AsyncIOMotorDatabase = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    verified_only: bool = False
):
    """Get all sellers (with optional verified filter)"""
    query = {"is_active": True}
    if verified_only:
        query["is_verified"] = True
    
    sellers = await db.sellers.find(
        query,
        {"_id": 0}
    ).skip(skip).limit(limit).to_list(limit)
    return sellers
