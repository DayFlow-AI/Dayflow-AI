from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)
from fastapi.logger import logger
from sqlalchemy.exc import SQLAlchemyError

from db_conf.db import SessionDep
from plan_board.utils import access_security

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: SessionDep,
):
    user = await access_security(websocket.cookies)
    if not user:
        raise WebSocketException(code=1008, reason="invalid credentials")

    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"message": f"hello mister {user}"})
            await websocket.receive_json()
    except WebSocketDisconnect:
        await websocket.close(reason="websocket connection closed")

    except SQLAlchemyError as e:
        logger.info(e)
        await websocket.close(code=1011, reason="server db exception")
