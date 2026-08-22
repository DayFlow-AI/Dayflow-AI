from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Depends
from fastapi_jwt import JwtAuthorizationCredentials

from db_conf.db import SessionDep
from user.utils import access_security

ws_router = APIRouter(prefix="/ws")


@ws_router.websocket("")
async def websocket_endpoint(websocket: WebSocket, db: SessionDep, credentials: JwtAuthorizationCredentials = Depends(
    access_security)):
    if credentials:
        await websocket.accept()
    try:
        while True:
            await websocket.send_json({"message": "hello, websocket connection established from test"})
            await websocket.send_json({"message": 'send ping in {"message": "ping"} to debugging'})
            await websocket.receive_json("message")
    except WebSocketDisconnect:
        await websocket.close(reason="websocket connection closed")

    except Exception as e:
        await websocket.close(reason=str(e), code=1011)
