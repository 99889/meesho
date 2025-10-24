import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

async def fix_admin_user():
    # MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update admin users to include created_at and updated_at fields
    result = await db.users.update_many(
        {'role': 'admin'}, 
        {'$set': {
            'created_at': datetime.utcnow(), 
            'updated_at': datetime.utcnow()
        }}
    )
    
    print(f"Fixed {result.modified_count} admin users")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_admin_user())