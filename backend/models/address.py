from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
import uuid

class Address(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    phone: str
    email: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    address_type: Literal['home', 'work', 'other'] = 'home'
    is_default: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AddressCreate(BaseModel):
    name: str
    phone: str
    email: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    address_type: Literal['home', 'work', 'other'] = 'home'
    is_default: bool = False

class AddressUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    address_type: Optional[Literal['home', 'work', 'other']] = None
    is_default: Optional[bool] = None

class AddressResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    pincode: str
    address_type: str
    is_default: bool
    created_at: datetime
