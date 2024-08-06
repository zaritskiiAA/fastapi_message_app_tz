from datetime import datetime
from typing import Optional

from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, ConfigDict

from .validators import text_cannot_be_null


class MessageBase(BaseModel):

    text: Annotated[str, BeforeValidator(text_cannot_be_null)] 
    username: str = 'Anonim'


class MessageCreate(MessageBase):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "text": "Input your message here.",
            }
        },
    )


class MessageDB(MessageBase):

    id: Optional[Annotated[str, BeforeValidator(str)]] = Field(
        alias='_id', default=None,
    )
    create_datetime: Optional[datetime] = None


class MessageDBList(BaseModel):

    messages: list[MessageDB]