from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.category import Category, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])

async def get_db():
    from server import db
    return db

@router.get("")
async def get_categories(db: AsyncIOMotorDatabase = Depends(get_db)):
    categories = await db.categories.find({}, {"_id": 0}).to_list(100)
    return {"categories": categories}

@router.post("")
async def create_category(
    category_data: CategoryCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    category = Category(**category_data.dict())
    await db.categories.insert_one(category.dict())
    return {"category": category.dict()}
