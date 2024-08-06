from datetime import datetime

from .base import CRUDBase


class MessagesCRUD(CRUDBase):

    async def create_document(self, data: dict) -> None:
        data['create_datetime'] = datetime.now()
        return await super().create_document(data)


