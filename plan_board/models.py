from sqlalchemy.orm import relationship

from db_conf.db import Base

class Websockets(Base):
    __tablename__ = "websockets"
    user_id = relationship("User", back_populates="websockets")

