from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from db_conf.db import SessionDep
from global_utils import AccessCredentials
from plan_board.models import ChatORM
from plan_board.schemas import ChatOutSchema, ChatSchema, ListChatOutSchema

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
async def add_board(
    db: SessionDep, credentials: AccessCredentials, incoming_data: ChatSchema
) -> ChatOutSchema:

    try:
        answer = (
            await db.execute(
                insert(ChatORM).values(
                    title=incoming_data.title, owner_id=int(credentials["uid"])
                ).returning(ChatORM.id, ChatORM.title)
            )
        ).first()
        await db.commit()
    except SQLAlchemyError as e:
        logger.error(e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Server Side Error")

    return ChatOutSchema.model_validate(answer)


@plan_board_router.get(
    "/get_boards",
    response_model=ListChatOutSchema,
    responses={
        500: {"description": "Server Error"},
        401: {"description": "Unauthorized"},
        404: {"description": "Empty list"},
    },
)
async def plan_board_add(
    db: SessionDep, credentials: AccessCredentials
) -> ListChatOutSchema:
    try:
        answer = (
            (
                await db.execute(
                    select(ChatORM).where(ChatORM.owner_id == int(credentials["uid"]))
                )
            )
            .scalars()
            .all()
        )
        if answer is None:
            answer = []
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Server Side Error")

    if answer is None:
        raise HTTPException(status_code=404, detail="Empty list")

    return ListChatOutSchema(chats=answer)
