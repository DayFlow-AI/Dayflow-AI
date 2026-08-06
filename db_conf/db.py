from dotenv import load_dotenv
from os import getenv as gv
from urllib.parse import quote_plus
from datetime import datetime
from fastapi import Depends
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated

load_dotenv()

db_pass = quote_plus(gv("DB_PASS"))
db_user = gv("DB_USER")
db_schema = gv("DB_SCHEMA")

if not all([db_user, db_pass, db_schema]):
    raise RuntimeError("environment variables not set check env file")

db_url = f"postgresql+psycopg://{db_user}:{db_pass}@localhost:5432/{db_schema}"
engine = create_async_engine(db_url)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as conn:
        yield conn


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
