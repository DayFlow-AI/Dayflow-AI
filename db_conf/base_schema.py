from pydantic import BaseModel


class CustomSchema(BaseModel):
    ...


class CustomOutSchema(CustomSchema):
    id: int
