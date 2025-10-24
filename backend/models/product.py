from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    discount: Optional[float] = 0
    category: str
    images: Optional[List[str]] = []  # Main images for slideshow
    additionalImages: Optional[List[str]] = []  # Additional images
    pdfDocuments: Optional[List[str]] = []  # PDF documents
    sizes: List[str] = []
    colors: List[str] = []
    rating: float = 0.0
    reviews: int = 0
    free_delivery: bool = True
    cod: bool = True
    seller_id: Optional[str] = None
    seller_name: Optional[str] = None
    return_policy: str = "7 days return"
    stock: int = 100
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    discount: Optional[float] = 0
    category: str
    images: Optional[List[str]] = []  # Main images for slideshow
    additionalImages: Optional[List[str]] = []  # Additional images
    pdfDocuments: Optional[List[str]] = []  # PDF documents
    sizes: List[str] = []
    colors: List[str] = []
    rating: float = 0.0
    reviews: int = 0
    free_delivery: bool = True
    cod: bool = True
    seller_name: Optional[str] = None
    return_policy: str = "7 days return"
    stock: int = 100

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    discount: Optional[float] = None
    category: Optional[str] = None
    images: Optional[List[str]] = None  # Main images for slideshow
    additionalImages: Optional[List[str]] = None  # Additional images
    pdfDocuments: Optional[List[str]] = None  # PDF documents
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    stock: Optional[int] = None
    seller_name: Optional[str] = None
    return_policy: Optional[str] = None
    free_delivery: Optional[bool] = None
    cod: Optional[bool] = None