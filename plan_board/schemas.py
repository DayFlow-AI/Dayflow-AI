from pydantic import BaseModel, ConfigDict, Field


class ChatSchema(BaseModel):
    title: str


class ChatOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


class ListChatOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    chats: list[ChatOutSchema] = Field(default_factory=list)