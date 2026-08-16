from fastapi import HTTPException, Response, APIRouter, status, Depends
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select, exists, or_, delete
from db_conf.db import SessionDep
from user.models import UsersORM, UsersJWTStorageORM
from user.schemas import UserRegisterSchema, UserLoginSchema, AuthSuccessSchema, UserPublicSchema
from user.utils import conf, hashing, password_hash, gen_jwt, access_security

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post(
    "/register",
    summary="create and auth user",
    response_model=AuthSuccessSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "user already exists"},
    },
)
async def register(user: UserRegisterSchema, db: SessionDep) -> Response:
    query = select(exists().where(
        or_(
            UsersORM.email == user.email, UsersORM.username == user.username
        )
    ))
    exists_result = await db.execute(query)
    if not exists_result.scalar():
        new_user = await hashing(user, db)
        jwt = await gen_jwt(new_user, db)
        response = Response(status_code=status.HTTP_201_CREATED)
        response.set_cookie(**conf(jwt))
        return response
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already registered")


@router.post(
    "/login",
    summary="Login a user",
    response_model=AuthSuccessSchema,
    responses={
        401: {"description": "Incorrect password"},
        400: {"description": "Incorrect email or username"},
    },
)
async def login_user(login: UserLoginSchema, db: SessionDep) -> Response:
    query = select(UsersORM).where(
        or_(
            UsersORM.email == login.login, UsersORM.username == login.login
        )
    )
    exists_login = await db.execute(query)
    exists_login = exists_login.scalar()
    if exists_login:
        access = password_hash.verify(login.password, exists_login.password)
        if access:
            jwt = await gen_jwt(exists_login, db)
            response = Response(status_code=status.HTTP_200_OK)
            response.set_cookie(**conf(jwt))
            return response
        raise HTTPException(status_code=401, detail="Incorrect password")
    raise HTTPException(status_code=400, detail="Incorrect email or username")


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "no content"},
        401: {"description": "not authorized / session expired"},
    },
)
async def logout(db: SessionDep, credentials: JwtAuthorizationCredentials = Depends(access_security)) -> Response:
    await db.execute(
        delete(UsersJWTStorageORM).where(UsersJWTStorageORM.jwt_token == credentials.jti)
    )
    await db.commit()
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    access_security.unset_access_cookie(response)
    return response


@router.post(
    "/logout_from_all_devices",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "no content"},
        401: {"description": "not authorized / session expired"},
    },
)
async def logout_from_all_devices(db: SessionDep,
                                  credentials: JwtAuthorizationCredentials = Depends(access_security)) -> Response:
    user_id = int(credentials.subject["uid"])
    await db.execute(
        delete(UsersJWTStorageORM).where(UsersJWTStorageORM.user_id == user_id)
    )
    await db.commit()
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    access_security.unset_access_cookie(response)
    return response


@router.get(
    "/me",
    response_model=UserPublicSchema,
    status_code=status.HTTP_200_OK,
    summary="get current user",
    response_description="Authorized: user data. 401 - not authorized/session expired",
    responses={
        401: {"description": "not authorized / session expired"}
    },
)
async def me(db: SessionDep, credentials: JwtAuthorizationCredentials = Depends(access_security)) -> UserPublicSchema:
    user = (await db.execute(
        select(UsersORM).where(UsersORM.id == int(credentials.subject["uid"]))
    )).scalar_one()
    return UserPublicSchema.model_validate(user)
