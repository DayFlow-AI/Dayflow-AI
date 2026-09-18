from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_conf.db import Base


class UsersORM(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    oauth: Mapped[bool] = mapped_column(default=False, nullable=True)
    google_refresh_token: Mapped[str] = mapped_column(nullable=True)
    google_sub: Mapped[str] = mapped_column(nullable=True, index=True, unique=True)
    jwt_tokens: Mapped[list[UsersJWTStorageORM]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UsersJWTStorageORM(Base):
    __tablename__ = "user_jwt_storage"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    refresh_jti: Mapped[str]
    exp: Mapped[int] = mapped_column(BigInteger)
    user: Mapped[UsersORM] = relationship(back_populates="jwt_tokens")
