import asyncio
from contextlib import asynccontextmanager
from logging import info

from fastapi import FastAPI

from api.routers import main_router
from core.config import settings
from crud.db_config import mongo_db, init_redis_pool
from services.tg_bot import start_polling


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.database = mongo_db 
    app.cache = await init_redis_pool()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield

    app.mongodb_client.close()

app = FastAPI(
    title=settings.app_title, 
    description=settings.app_description, 
    lifespan=db_lifespan,
)
app.include_router(main_router)

if __name__ == "__main__":
    asyncio.run(start_polling())