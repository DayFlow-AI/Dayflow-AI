from pydantic import BaseModel


class ChatSchema(BaseModel):
    title_test: str


class ChatOutSchema(BaseModel):
    id: int
    title: str
