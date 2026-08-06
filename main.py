import uvicorn
from fastapi import FastAPI
from db import engine, Base
from user.routes import router as user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run(app, host="172.30.88.250", port=8000)
