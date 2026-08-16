from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_conf.db import Base


class UsersORM(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None]
    email: Mapped[str]
    jwt_tokens: Mapped[list["UsersJWTStorageORM"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

class UsersJWTStorageORM(Base):
    __tablename__ = "user_jwt_storage"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    username: Mapped[str]
    device_type: Mapped[str | None] = mapped_column(default="undefined-device")
    jwt_token: Mapped[str]
    user : Mapped["UsersORM"] = relationship(back_populates="jwt_tokens")