from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from fastapi.staticfiles import StaticFiles

# Import routes
from routes import auth, products, categories, orders, payments, reviews, addresses, coupons, sellers, admin, upload

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Meesho API Starting...")
    logger.info(f"📦 Database: {os.environ['DB_NAME']}")
    logger.info("✅ API Ready!")
    
    yield
    
    # Shutdown
    client.close()
    logger.info("👋 Shutting down...")

# Create the main app without a prefix
app = FastAPI(lifespan=lifespan)

# ADD CORS MIDDLEWARE FIRST (before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add basic health check
@api_router.get("/")
async def root():
    return {"message": "Meesho API is running", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    try:
        # Check MongoDB connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Include all routers
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)
api_router.include_router(reviews.router)
api_router.include_router(addresses.router)
api_router.include_router(coupons.router)
api_router.include_router(sellers.router)
api_router.include_router(admin.router)
api_router.include_router(upload.router)

# Include the router in the main app
app.include_router(api_router)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")