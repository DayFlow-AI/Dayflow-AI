from fastapi import HTTPException, Response, APIRouter, Depends
from sqlalchemy import select
from db import SessionDep
from user.models import UsersORM
from user.schemas import UserSchema, UserLoginSchema
from authx import AuthX, AuthXConfig
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/get/")
async def users(data: UserSchema, session: SessionDep):
    query = select(UsersORM)
    result = await session.execute(query)
    return result.scalars().all()


config = AuthXConfig()
security = AuthX(config=config)


@router.post("/login/")
async def login(credentials: UserLoginSchema, response: Response):
    if credentials.email and credentials.password:
        token = security.create_access_token(uid='12321')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.get("/protected/", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"message": "Hello World"}
