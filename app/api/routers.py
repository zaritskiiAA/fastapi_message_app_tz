from fastapi import APIRouter

from api.endpoints import message_router
from constants import API_VERSION


main_router = APIRouter()
main_router.include_router(
    message_router, prefix=f'/api/{API_VERSION}/messages', tags=['Messages'],
)

