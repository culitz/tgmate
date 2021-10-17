from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query
from tgmate.models import User

from .base import BaseController


class UserController(BaseController):
    def __init__(self, engine: Engine, _session: Optional[Session] = None) -> None:
        super().__init__(engine, User, _session)