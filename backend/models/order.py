from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime
import uuid

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    selected_size: str
    selected_color: str
    image: str

class ShippingAddress(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    city: str
    state: str
    pincode: str

class PaymentDetails(BaseModel):
    upi_id: Optional[str] = None
    transaction_id: Optional[str] = None

class TrackingEvent(BaseModel):
    status: Literal['pending', 'confirmed', 'shipped', 'out_for_delivery', 'delivered', 'cancelled']
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = None
    description: Optional[str] = None

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: Literal['cod', 'upi', 'card', 'netbanking']
    payment_details: Optional[PaymentDetails] = None
    payment_status: Literal['pending', 'completed', 'failed'] = 'pending'
    order_status: Literal['pending', 'confirmed', 'shipped', 'out_for_delivery', 'delivered', 'cancelled'] = 'pending'
    tracking_events: List[TrackingEvent] = []
    total_amount: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: Literal['cod', 'upi', 'card', 'netbanking']
    payment_details: Optional[PaymentDetails] = None
    total_amount: float