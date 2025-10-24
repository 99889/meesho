from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime
import uuid

class SellerProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str  # Reference to user
    shop_name: str
    shop_description: Optional[str] = None
    shop_logo: Optional[str] = None
    rating: float = 0.0  # Average rating
    total_reviews: int = 0
    total_products: int = 0
    response_time: Optional[str] = None  # e.g., "within 24 hours"
    is_verified: bool = False
    is_active: bool = True
    bank_account: Optional[str] = None  # Masked for security
    commission_rate: float = 0.0  # Commission percentage
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SellerProfileCreate(BaseModel):
    shop_name: str
    shop_description: Optional[str] = None
    shop_logo: Optional[str] = None

class SellerProfileUpdate(BaseModel):
    shop_name: Optional[str] = None
    shop_description: Optional[str] = None
    shop_logo: Optional[str] = None
    response_time: Optional[str] = None

class SellerReview(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    seller_id: str
    user_id: str
    order_id: str
    rating: int  # 1-5
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SellerReviewCreate(BaseModel):
    seller_id: str
    order_id: str
    rating: int  # 1-5
    comment: str

class SellerReviewResponse(BaseModel):
    id: str
    seller_id: str
    user_id: str
    rating: int
    comment: str
    created_at: datetime

class SellerProfileResponse(BaseModel):
    id: str
    shop_name: str
    shop_description: Optional[str]
    shop_logo: Optional[str]
    rating: float
    total_reviews: int
    total_products: int
    response_time: Optional[str]
    is_verified: bool
    created_at: datetime
