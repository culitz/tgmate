from .base import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from config import TABLENAME_TASK


class Task(Base):
    __tablename__ = TABLENAME_TASK
    # Local task id
    id = Column(Integer, primary_key=True)
    # Publish date
    date = Column(DateTime, nullable=False)
    # Publish status True -> done, False -> not yet
    status = Column(Boolean, default=False)
    # Telegram user's id who was forwarded message to bot
    author = Column(Integer, nullable=False)
    # Message to forward
    message = relationship("Message")