from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDB:

    client: AsyncIOMotorClient = None

    @classmethod
    async def connect_db(cls):
        try:
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                maxPoolSize=50,
                minPoolSize=10,
                serverSelectionTimeoutMS=5000,
                uuidRepresentation="standard"
            )

            # Verify connection
            await cls.client.admin.command("ping")

            logger.info("MongoDB Connected Successfully")

        except Exception as e:
            logger.error(f"MongoDB Connection Error: {e}")
            raise e

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            logger.info("MongoDB Connection Closed")

    @classmethod
    def get_database(cls):
        return cls.client[settings.DATABASE_NAME]