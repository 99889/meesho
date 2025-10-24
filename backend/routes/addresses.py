from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.address import Address, AddressCreate, AddressUpdate, AddressResponse
from middleware.auth import get_current_user
from typing import List

router = APIRouter(prefix="/addresses", tags=["addresses"])

async def get_db():
    from server import db
    return db

@router.post("", response_model=AddressResponse)
async def create_address(
    address: AddressCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new address for the current user"""
    new_address = Address(
        user_id=current_user["id"],
        **address.dict()
    )
    
    # If this is the default address, unset other defaults
    if new_address.is_default:
        await db.addresses.update_many(
            {"user_id": current_user["id"]},
            {"$set": {"is_default": False}}
        )
    
    result = await db.addresses.insert_one(new_address.dict())
    new_address.id = str(result.inserted_id)
    return new_address

@router.get("", response_model=List[AddressResponse])
async def get_addresses(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all addresses for the current user"""
    addresses = await db.addresses.find(
        {"user_id": current_user["id"]},
        {"_id": 0}
    ).to_list(None)
    return addresses

@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get a specific address"""
    address = await db.addresses.find_one(
        {"id": address_id, "user_id": current_user["id"]},
        {"_id": 0}
    )
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: str,
    address_update: AddressUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update an address"""
    update_data = {k: v for k, v in address_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # If setting as default, unset other defaults
    if update_data.get("is_default"):
        await db.addresses.update_many(
            {"user_id": current_user["id"], "id": {"$ne": address_id}},
            {"$set": {"is_default": False}}
        )
    
    result = await db.addresses.update_one(
        {"id": address_id, "user_id": current_user["id"]},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    
    updated_address = await db.addresses.find_one(
        {"id": address_id},
        {"_id": 0}
    )
    return updated_address

@router.delete("/{address_id}")
async def delete_address(
    address_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Delete an address"""
    result = await db.addresses.delete_one(
        {"id": address_id, "user_id": current_user["id"]}
    )
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return {"message": "Address deleted successfully"}

@router.get("/default/get", response_model=AddressResponse)
async def get_default_address(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get the default address for the current user"""
    address = await db.addresses.find_one(
        {"user_id": current_user["id"], "is_default": True},
        {"_id": 0}
    )
    if not address:
        raise HTTPException(status_code=404, detail="No default address found")
    return address
