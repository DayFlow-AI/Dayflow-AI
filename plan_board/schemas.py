from pydantic import BaseModel, ConfigDict, Field


class ChatSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


class ChatCreateSchema(BaseModel):
    title: str


class ListChatOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    chats: list[ChatSchema] = Field(default_factory=list)
