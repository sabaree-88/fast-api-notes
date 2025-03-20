from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# Initialize MongoDB client
client = AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.DATABASE_NAME]

# Collections
users_collection = database.get_collection("users")
notes_collection = database.get_collection("notes")

# Dependency for FastAPI
async def get_db():
    """Provides a database connection as a dependency in FastAPI routes."""
    yield database  # Async generator (best practice)
