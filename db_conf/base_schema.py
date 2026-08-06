from pydantic import BaseModel


class CustomSchema(BaseModel):
    """База для входных схем: id назначает БД, клиент его не шлёт."""


class CustomOutSchema(CustomSchema):
    """База для выходных схем: id отдаётся наружу."""
    id: int
