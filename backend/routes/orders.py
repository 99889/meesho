from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.order import Order, OrderCreate, TrackingEvent
from middleware.auth import get_current_user
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Literal

router = APIRouter(prefix="/orders", tags=["orders"])

async def get_db():
    from server import db
    return db

@router.post("")
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    # Create initial tracking event
    initial_tracking = TrackingEvent(
        status="pending",
        description="Order placed successfully"
    )
    
    order = Order(
        **order_data.dict(),
        user_id=current_user["user_id"],
        tracking_events=[initial_tracking]
    )
    
    await db.orders.insert_one(order.dict())
    return {"order": order.dict()}

# New endpoint for guest orders
@router.post("/guest")
async def create_guest_order(
    order_data: OrderCreate,
    db = Depends(get_db)
):
    # Generate a unique user ID for guest
    guest_user_id = f"guest_{str(uuid.uuid4())}"
    
    # Create initial tracking event
    initial_tracking = TrackingEvent(
        status="pending",
        description="Order placed successfully"
    )
    
    order = Order(
        **order_data.dict(),
        user_id=guest_user_id,
        tracking_events=[initial_tracking]
    )
    
    await db.orders.insert_one(order.dict())
    return {"order": order.dict(), "guest_user_id": guest_user_id}

@router.get("")
async def get_orders(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    orders = await db.orders.find({"user_id": current_user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"orders": orders}

class OrderStatusUpdate(BaseModel):
    status: Literal['pending', 'confirmed', 'shipped', 'out_for_delivery', 'delivered', 'cancelled']
    location: Optional[str] = None
    description: Optional[str] = None

@router.get("/{order_id}")
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    order = await db.orders.find_one({"id": order_id, "user_id": current_user["user_id"]}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order": order}

@router.post("/{order_id}/track")
async def update_order_tracking(
    order_id: str,
    tracking_update: OrderStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    # In a real application, this would be restricted to admins/sellers
    # For now, we'll allow it for demonstration purposes
    order = await db.orders.find_one({"id": order_id, "user_id": current_user["user_id"]})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Create new tracking event
    new_tracking = TrackingEvent(
        status=tracking_update.status,
        location=tracking_update.location,
        description=tracking_update.description
    )
    
    # Update order status and add tracking event
    await db.orders.update_one(
        {"id": order_id},
        {
            "$set": {
                "order_status": tracking_update.status,
                "updated_at": datetime.utcnow()
            },
            "$push": {
                "tracking_events": new_tracking.dict()
            }
        }
    )
    
    # Fetch updated order
    updated_order = await db.orders.find_one({"id": order_id}, {"_id": 0})
    return {"order": updated_order}