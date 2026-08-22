import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from plan_board.ws import ws_router
from user.routes import router as user_router
from user.oauth2_0.routes import oauth2_router

app = FastAPI(debug=True, title="DayFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://172.30.88.252:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(oauth2_router)
app.include_router(ws_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="172.30.88.250", port=8000)
