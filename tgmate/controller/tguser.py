from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query
from tgmate.models import TgUser
from .base import BaseController


class TgUserController(BaseController):
    def __init__(self, engine: Engine, _session: Optional[Session] = None) -> None:
        super().__init__(engine, TgUser, _session)