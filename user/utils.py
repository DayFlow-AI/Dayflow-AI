from uuid import uuid4
from fastapi import HTTPException, Depends, status
from fastapi_jwt import JwtAccessBearerCookie, JwtAuthorizationCredentials
from pwdlib import PasswordHash
from sqlalchemy import select
from user.schemas import UserRegisterSchema
from user.models import UsersORM, UsersJWTStorageORM
from db_conf.db import SessionDep
from proj_settings.env_conf import settings

sec_key = settings.jwt_secret_key
password_hash = PasswordHash.recommended()
access_security = JwtAccessBearerCookie(secret_key=sec_key, auto_error=False)


def conf(jwt) -> dict:
    secure = settings.jwt_secure
    return {
        "key": "access_token_cookie",
        "value": jwt,
        "httponly": True,
        "secure": secure,
        "samesite": "lax",
        "max_age": 900,
        "path": "/",
    }


async def hashing(user: UserRegisterSchema, db: SessionDep) -> UsersORM:
    try:
        hashed = password_hash.hash(user.password)
        new_user = UsersORM(username=user.username, email=user.email, password=hashed)
        db.add(new_user)
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return new_user


async def gen_jwt(hashed_user: UsersORM, db: SessionDep) -> str:
    try:
        jti = str(uuid4())
        jwt = access_security.create_access_token(
            subject={"uid": str(hashed_user.id)},
            unique_identifier=jti,
        )
        db.add(UsersJWTStorageORM(user_id=hashed_user.id, username=hashed_user.username, jwt_token=jti))
        await db.commit()
        return jwt
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Cannot create new jwt")


async def require_valid_session(db: SessionDep, credentials: JwtAuthorizationCredentials = Depends(
    access_security)) -> JwtAuthorizationCredentials:
    session = (await db.execute(
        select(UsersJWTStorageORM).where(UsersJWTStorageORM.jwt_token == credentials.jti)
    )).scalar_one_or_none()
    if session is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Session revoked")
    return credentials