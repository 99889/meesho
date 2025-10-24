import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
from utils.auth import get_password_hash
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

async def create_admin_user():
    # MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    from datetime import datetime
    
    # Admin user data
    admin_data = {
        "id": str(uuid.uuid4()),
        "name": "Admin User",
        "email": "admin@meesho.com",
        "password": get_password_hash("admin123"),
        "phone": "9999999999",
        "role": "admin",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"email": admin_data["email"]})
    if existing_admin:
        print("Admin user already exists!")
        await client.close()
        return
    
    # Create admin user
    await db.users.insert_one(admin_data)
    print("Admin user created successfully!")
    print("Email: admin@meesho.com")
    print("Password: admin123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin_user())