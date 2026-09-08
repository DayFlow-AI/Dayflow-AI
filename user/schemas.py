from pydantic import ConfigDict, EmailStr, Field

from db_conf.base_schema import CustomSchema


class UserPublicSchema(CustomSchema):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str = Field(max_length=100)
    oauth: bool = Field(default=False)


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


class ChangePasswordSchema(CustomSchema):
    current_password: str = Field(max_length=100)
    new_password: str = Field(max_length=100)


class PasswordResponseSchema(CustomSchema):
    detail: str = Field(examples=["Password changed successfully, please log in again"])
