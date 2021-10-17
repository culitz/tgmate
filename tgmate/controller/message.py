from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tgmate.models import Message
from .base import BaseController


class MessageController(BaseController):
    def __init__(self, engine: Engine, _session: Optional[Session] = None):
        super().__init__(engine, Message)
