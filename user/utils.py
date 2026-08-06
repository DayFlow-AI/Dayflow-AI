from uuid import uuid4
from fastapi import HTTPException
from fastapi_jwt import JwtAccessBearerCookie
from pwdlib import PasswordHash
from user.schemas import UserRegisterSchema
from user.models import UsersORM, UsersJWTStorageORM
from db_conf.db import SessionDep
from dotenv import load_dotenv
from os import getenv as gv

load_dotenv()
sec_key = str(gv("JWT_SECRET_KEY"))
password_hash = PasswordHash.recommended()
access_security = JwtAccessBearerCookie(secret_key=sec_key)


def conf(jwt) -> dict:
    # secure=True только по HTTPS, иначе браузер молча не сохранит куку
    secure = gv("JWT_SECURE", "False").lower() == "true"
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
    jti = str(uuid4())
    jwt = access_security.create_access_token(
        subject={"uid": str(hashed_user.id)},
        unique_identifier=jti,
    )
    db.add(UsersJWTStorageORM(user_id=hashed_user.id, username=hashed_user.username, jwt_token=jti))
    await db.commit()
    return jwt
