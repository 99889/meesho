from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User, UserCreate, UserLogin, UserResponse
from utils.auth import get_password_hash, verify_password, create_access_token
from middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

async def get_db():
    from server import db
    return db

@router.post("/register")
async def register(user_data: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        phone=user_data.phone,
        role=user_data.role
    )
    
    await db.users.insert_one(user.dict())
    
    # Create token
    token = create_access_token(data={"user_id": user.id, "email": user.email})
    
    return {
        "token": token,
        "user": UserResponse(**user.dict()).dict()
    }

@router.post("/login")
async def login(credentials: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Find user
    user_data = await db.users.find_one({"email": credentials.email})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token = create_access_token(data={"user_id": user_data["id"], "email": user_data["email"]})
    
    user_response = UserResponse(**user_data)
    
    return {
        "token": token,
        "user": user_response.dict()
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    user_data = await db.users.find_one({"id": current_user["user_id"]})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user": UserResponse(**user_data).dict()}
