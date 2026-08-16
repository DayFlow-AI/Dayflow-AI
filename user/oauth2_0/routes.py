from fastapi import status, APIRouter
from db_conf.db import SessionDep
from proj_settings.env_conf import settings
from authlib.integrations.httpx_client import AsyncOAuth2Client
from user.oauth2_0.schemas import OauthSchema

oauth2_router = APIRouter(prefix="/api/oauth2", tags=["oauth2"])

client = AsyncOAuth2Client(
    client_id=settings.client_id,
    client_secret=settings.client_sec,
    redirect_uri=settings.redirect_uri,
)


@oauth2_router.post("/auth/callback", status_code=status.HTTP_200_OK)
async def auth_callback(code: OauthSchema, db: SessionDep):
    token = await client.fetch_token(
        "https://oauth2.googleapis.com/token",
        code=code.code,
        grant_type="authorization_code",
    )
    return {"access_token": token["access_token"], "token_type": "bearer"}
