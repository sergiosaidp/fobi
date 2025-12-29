from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes.chatbots import router as chatbots_router
from routes.conversations import router as conversations_router
from routes.stats import router as stats_router


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'fobi_clone')]

# Create the main app without a prefix
app = FastAPI(
    title="Fobi.io Clone API",
    description="API for creating chatbots from Google Forms",
    version="1.0.0"
)

# Create a router with the /api prefix for general routes
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Fobi.io Clone API",
        "status": "healthy",
        "version": "1.0.0"
    }

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Include the general router
app.include_router(api_router)

# Include feature-specific routers
app.include_router(chatbots_router)
app.include_router(conversations_router)
app.include_router(stats_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()