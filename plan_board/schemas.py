from pydantic import BaseModel


class ChatSchema(BaseModel):
    title: str


class ChatOutSchema(BaseModel):
    id: int
    title: str
