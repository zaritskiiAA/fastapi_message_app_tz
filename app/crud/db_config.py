from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from core.config import settings


mongo_client = AsyncIOMotorClient(settings.mongo_url)
mongo_db = mongo_client.get_default_database()


async def init_redis_pool() -> redis.Redis:
    redis_cli = await redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        db=settings.redis_db,
        decode_responses=True,
    )
    return redis_cli