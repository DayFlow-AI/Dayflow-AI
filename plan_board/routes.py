from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from db_conf.db import SessionDep
from global_utils import AccessCredentials
from plan_board.models import ChatORM
from plan_board.schemas import ChatOutSchema, ChatSchema
from user.models import UsersORM

plan_board_router = APIRouter(prefix="/api/board", tags=["PlanBoard"])


@plan_board_router.post(
    "/add_board",
    response_model=ChatOutSchema,
    responses={
        500: {"description": "Server Error"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
    },
)
async def plan_board_add(
    db: SessionDep, credentials: AccessCredentials, incoming_data: ChatSchema
) -> HTTPException | ChatOutSchema:

    user = await db.get(UsersORM, UsersORM.id == int(credentials["uid"]))
    try:
        await db.execute(
            insert(ChatORM).values(
                title=incoming_data.title, owner_id=int(credentials["uid"])
            )
        )
        await db.commit()
    except SQLAlchemyError as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))

    return ChatOutSchema.model_validate(user)
