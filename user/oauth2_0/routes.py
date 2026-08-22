from datetime import datetime
from authlib.integrations.base_client import OAuthError
from fastapi import status, APIRouter, HTTPException, Response
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from db_conf.db import SessionDep
from proj_settings.env_conf import settings
from authlib.integrations.httpx_client import AsyncOAuth2Client
from user.models import UsersORM
from user.oauth2_0.schemas import OauthSchema
from user.oauth2_0.utils import get_google_profile
from user.utils import gen_jwt, conf
from fastapi.logger import logger

oauth2_router = APIRouter(prefix="/api/oauth2", tags=["oauth2"])

client = AsyncOAuth2Client(
    client_id=settings.client_id,
    client_secret=settings.client_sec,
    redirect_uri=settings.redirect_uri,
    scope=settings.user_scopes,
)


@oauth2_router.post("/auth/callback", status_code=status.HTTP_200_OK)
async def auth_callback(code: OauthSchema, db: SessionDep) -> Response:
    try:
        token = await client.fetch_token(
            "https://oauth2.googleapis.com/token",
            code=code.code,
            grant_type="authorization_code",
        )
        user_data = await get_google_profile(token["access_token"])
        query = insert(UsersORM).values(
            username=user_data.name,
            email=user_data.email,
            google_sub=user_data.sub,
            oauth=True,
            google_refresh_token=token["refresh_token"],
        ).on_conflict_do_update(
            index_elements=["google_sub"],
            set_={"username": user_data.name,
                  "email": user_data.email,
                  "google_refresh_token": token["refresh_token"],
                  "updated_at": datetime.now()
                  },
        ).returning(UsersORM.id)
        result = await db.execute(query)
        result = result.scalar_one()
        user = select(UsersORM).where(UsersORM.id == result)
        result = await db.execute(user)
        result = result.scalar_one()
        jwt = await gen_jwt(result, db)
        response = Response(status_code=status.HTTP_200_OK)
        response.set_cookie(**conf(jwt))

    except OAuthError as e:
        await db.rollback()
        logger.info("OAuthError info: %s", e.description)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"error: OAuth authentication failed")

    except ValidationError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Validation Error")

    except Exception as e:
        await db.rollback()
        logger.error("Other mistakes: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Other mistakes")

    else:
        return response
