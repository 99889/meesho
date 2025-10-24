from fastapi import APIRouter, HTTPException, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.coupon import Coupon, CouponCreate, CouponValidate, CouponResponse, CouponValidationResponse
from middleware.auth import get_current_user
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/coupons", tags=["coupons"])

async def get_db():
    from server import db
    return db

@router.post("", response_model=CouponResponse)
async def create_coupon(
    coupon: CouponCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new coupon (Admin only)"""
    # Check if user is admin (you can add role-based access control)
    new_coupon = Coupon(**coupon.dict())
    
    # Check if coupon code already exists
    existing = await db.coupons.find_one({"code": new_coupon.code})
    if existing:
        raise HTTPException(status_code=400, detail="Coupon code already exists")
    
    result = await db.coupons.insert_one(new_coupon.dict())
    new_coupon.id = str(result.inserted_id)
    return new_coupon

@router.get("", response_model=List[CouponResponse])
async def get_active_coupons(
    db: AsyncIOMotorDatabase = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all active coupons"""
    now = datetime.utcnow()
    coupons = await db.coupons.find(
        {
            "is_active": True,
            "valid_from": {"$lte": now},
            "valid_until": {"$gte": now}
        },
        {"_id": 0}
    ).skip(skip).limit(limit).to_list(limit)
    return coupons

@router.post("/validate")
async def validate_coupon(
    validation: CouponValidate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Validate a coupon code"""
    coupon = await db.coupons.find_one(
        {"code": validation.code},
        {"_id": 0}
    )
    
    if not coupon:
        return CouponValidationResponse(
            is_valid=False,
            message="Coupon code not found"
        )
    
    now = datetime.utcnow()
    
    # Check if coupon is active
    if not coupon.get("is_active"):
        return CouponValidationResponse(
            is_valid=False,
            message="Coupon is not active"
        )
    
    # Check validity period
    if coupon.get("valid_from") > now or coupon.get("valid_until") < now:
        return CouponValidationResponse(
            is_valid=False,
            message="Coupon has expired or not yet valid"
        )
    
    # Check minimum purchase amount
    if validation.cart_total < coupon.get("min_purchase_amount", 0):
        return CouponValidationResponse(
            is_valid=False,
            message=f"Minimum purchase amount of ₹{coupon.get('min_purchase_amount')} required"
        )
    
    # Calculate discount
    discount_type = coupon.get("discount_type")
    discount_value = coupon.get("discount_value")
    
    if discount_type == "percentage":
        discount_amount = (validation.cart_total * discount_value) / 100
    else:
        discount_amount = discount_value
    
    # Apply max discount limit if set
    max_discount = coupon.get("max_discount_amount")
    if max_discount and discount_amount > max_discount:
        discount_amount = max_discount
    
    final_amount = validation.cart_total - discount_amount
    
    return CouponValidationResponse(
        is_valid=True,
        message="Coupon applied successfully",
        discount_amount=discount_amount,
        final_amount=final_amount
    )

@router.get("/{coupon_code}", response_model=CouponResponse)
async def get_coupon(
    coupon_code: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get coupon details by code"""
    coupon = await db.coupons.find_one(
        {"code": coupon_code},
        {"_id": 0}
    )
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon

@router.put("/{coupon_id}", response_model=CouponResponse)
async def update_coupon(
    coupon_id: str,
    coupon_update: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update a coupon (Admin only)"""
    result = await db.coupons.update_one(
        {"id": coupon_id},
        {"$set": coupon_update}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    updated_coupon = await db.coupons.find_one(
        {"id": coupon_id},
        {"_id": 0}
    )
    return updated_coupon

@router.delete("/{coupon_id}")
async def delete_coupon(
    coupon_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Delete a coupon (Admin only)"""
    result = await db.coupons.delete_one({"id": coupon_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    return {"message": "Coupon deleted successfully"}
