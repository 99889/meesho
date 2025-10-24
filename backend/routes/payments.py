from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from middleware.auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["payments"])

async def get_db():
    from server import db
    return db

class UPIPayment(BaseModel):
    upi_id: str
    amount: float
    order_id: str

class PaymentVerification(BaseModel):
    transaction_id: str
    order_id: str
    status: str

@router.post("/upi/initiate")
async def initiate_upi_payment(
    payment_data: UPIPayment,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Initiate UPI payment - In production, this would integrate with payment gateway
    For demo, we'll simulate the payment flow
    """
    # Verify order exists
    order = await db.orders.find_one({"id": payment_data.order_id, "user_id": current_user["user_id"]})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Generate transaction ID
    transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
    
    # In production, you would:
    # 1. Integrate with UPI payment gateway (Razorpay, PayU, etc.)
    # 2. Generate payment request
    # 3. Return payment URL or QR code
    
    # For demo, we'll return a mock payment URL
    payment_url = f"upi://pay?pa={payment_data.upi_id}&pn=Meesho&am={payment_data.amount}&tn=Order{payment_data.order_id}&tr={transaction_id}"
    
    # Update order with payment details
    await db.orders.update_one(
        {"id": payment_data.order_id},
        {
            "$set": {
                "payment_details": {
                    "upi_id": payment_data.upi_id,
                    "transaction_id": transaction_id
                },
                "payment_status": "pending",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {
        "success": True,
        "transaction_id": transaction_id,
        "payment_url": payment_url,
        "qr_code": f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={payment_url}",
        "message": "Payment initiated. Complete payment using UPI app"
    }

@router.post("/verify")
async def verify_payment(
    verification: PaymentVerification,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Verify payment status - In production, this would check with payment gateway
    """
    order = await db.orders.find_one({"id": verification.order_id, "user_id": current_user["user_id"]})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # In production, verify with payment gateway
    # For demo, we'll accept the status from frontend
    
    payment_status = verification.status.lower()
    if payment_status not in ['completed', 'failed', 'pending']:
        payment_status = 'failed'
    
    order_status = 'confirmed' if payment_status == 'completed' else 'pending'
    
    await db.orders.update_one(
        {"id": verification.order_id},
        {
            "$set": {
                "payment_status": payment_status,
                "order_status": order_status,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {
        "success": payment_status == 'completed',
        "payment_status": payment_status,
        "order_status": order_status,
        "message": f"Payment {payment_status}"
    }

@router.get("/methods")
async def get_payment_methods():
    """
    Get available payment methods
    """
    return {
        "methods": [
            {
                "id": "upi",
                "name": "UPI",
                "description": "Pay using any UPI app (GPay, PhonePe, Paytm)",
                "enabled": True,
                "icon": "smartphone"
            },
            {
                "id": "cod",
                "name": "Cash on Delivery",
                "description": "Pay when you receive the product",
                "enabled": True,
                "icon": "banknote"
            }
        ]
    }
