from pydantic import EmailStr, Field, ConfigDict
from db_conf.base_schema import CustomSchema


class UserPublicSchema(CustomSchema):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str = Field(max_length=100)


class UserRegisterSchema(CustomSchema):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str = Field(max_length=100)
    password: str = Field(max_length=100)


class UserLoginSchema(CustomSchema):
    login: str = Field(max_length=100)
    password: str = Field(max_length=100)


class AuthSuccessSchema(CustomSchema):
    detail: str = Field(examples=["authenticated"])
    token_type: str = Field(examples=["bearer"])