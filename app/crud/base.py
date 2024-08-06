from motor.motor_asyncio import (
    AsyncIOMotorDatabase, AsyncIOMotorClient, AsyncIOMotorCursor,
)
from pymongo.results import InsertOneResult


class CRUDBase:
    def __init__(self, db: AsyncIOMotorDatabase, collection: str) -> None:

        self._collection: AsyncIOMotorClient = db.get_collection(collection)

    def get_all_document(self) -> AsyncIOMotorCursor:

        doc = self._collection.find({})
        return doc
    
    async def create_document(self, data: dict) -> InsertOneResult:

        insert_result = await self._collection.insert_one(data)
        return insert_result

    async def get_document_by_attr(self, attr: dict) -> dict:

        doc = await self._collection.find_one(attr)
        return doc
    
    async def clear(self) -> None:
        await self._collection.delete_many({})