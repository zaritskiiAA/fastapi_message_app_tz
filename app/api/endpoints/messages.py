import json

from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from schemas.messages import MessageCreate, MessageDB, MessageDBList
from constants import (
    DEF_PAGE, DEF_PAGINATION_LIMIT, 
    MSG_WITH_PAGINATE_CACHE_KEY, MSG_PATTERN,
)
from crud.messages import MessagesCRUD


router = APIRouter()


@router.get('/', response_model=MessageDBList)
async def get_messages(
    request: Request, page: int = DEF_PAGE, limit: int = DEF_PAGINATION_LIMIT,
):

    messages_collection: AsyncIOMotorClient = MessagesCRUD(
        request.app.database, 'messages',
    )
    cache_key = MSG_WITH_PAGINATE_CACHE_KEY.format(page=page, limit=limit)
    if page:
        page -= 1

    cache = await request.app.cache.get(cache_key)
    if cache:
        return json.loads(cache)
    
    cursor = messages_collection.get_all_document().skip(page * limit).limit(limit) # noqa E501
    result = []
    async for msg in cursor:
        result.append(msg)
    await request.app.cache.set(
        cache_key,
        MessageDBList(messages=result).model_dump_json(
            by_alias=True, exclude=["id"],
        )
    )
    return MessageDBList(messages=result)


@router.post('/', response_model=MessageDB)
async def send_message(request: Request, message: MessageCreate):
    
    keys = await request.app.cache.keys(MSG_PATTERN)
    messages_collection: AsyncIOMotorClient = MessagesCRUD(
        request.app.database, 'messages',
    )
    insert_msg = await messages_collection.create_document(
        message.model_dump(),
    )
    cur_msg = await messages_collection.get_document_by_attr(
        {'_id': insert_msg.inserted_id},
    )
    if keys:
        await request.app.cache.delete(*keys)
    return cur_msg