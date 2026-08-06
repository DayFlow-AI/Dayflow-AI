import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.routes import router as user_router

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

if __name__ == "__main__":
    uvicorn.run(app, host="172.30.88.250", port=8000)
