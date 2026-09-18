from pydantic import BaseModel


class ChatSchema(BaseModel):
    title_test_ci: str


class ChatOutSchema(BaseModel):
    id: int
    title: str
