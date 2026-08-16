from pydantic import BaseModel, ConfigDict


class OauthSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str


class UserOauthInfo(BaseModel):
    sub: str
    email: str
    name: str