from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    email: EmailStr
    username: str = Field(max_length=100)
    password: str = Field(max_length=100)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=100)