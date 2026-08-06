from dotenv import load_dotenv
from os import getenv as gv
from urllib.parse import quote_plus
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated

load_dotenv()

db_pass = quote_plus(gv("DB_PASS"))
db_user = gv("DB_USER")
db_schema = gv("DB_SCHEMA")

if not all([db_user, db_pass, db_schema]):
    raise RuntimeError("environment variables not set check env file")

engine = create_async_engine(f"postgresql+psycopg://{db_user}:{db_pass}@localhost:5432/{db_schema}")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as conn:
        yield conn


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass
