from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    tg_bot_token: str 
    app_title: str = 'Моковое приложение.'
    app_description: str = 'Приложение для чтения и отправки сообщения.'
    redis_url: str = 'redis://localhost'
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    mongo_url: str = 'mongodb://localhost:27017/local_database'
    secret: str = 'SECRET'

    class Config:
        env_file = '../.env'


settings = Settings()
