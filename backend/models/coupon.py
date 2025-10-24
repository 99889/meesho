from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
import uuid

class Coupon(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str  # Unique coupon code
    description: str
    discount_type: Literal['percentage', 'fixed'] = 'percentage'
    discount_value: float  # Percentage (0-100) or fixed amount
    min_purchase_amount: float = 0
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None  # Total uses allowed
    usage_per_user: int = 1  # Uses per user
    is_active: bool = True
    valid_from: datetime
    valid_until: datetime
    applicable_categories: Optional[list] = None  # Empty = all categories
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CouponCreate(BaseModel):
    code: str
    description: str
    discount_type: Literal['percentage', 'fixed'] = 'percentage'
    discount_value: float
    min_purchase_amount: float = 0
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_per_user: int = 1
    is_active: bool = True
    valid_from: datetime
    valid_until: datetime
    applicable_categories: Optional[list] = None

class CouponValidate(BaseModel):
    code: str
    cart_total: float
    user_id: Optional[str] = None

class CouponResponse(BaseModel):
    id: str
    code: str
    description: str
    discount_type: str
    discount_value: float
    min_purchase_amount: float
    max_discount_amount: Optional[float]
    is_active: bool
    valid_from: datetime
    valid_until: datetime

class CouponValidationResponse(BaseModel):
    is_valid: bool
    message: str
    discount_amount: float = 0
    final_amount: float = 0
