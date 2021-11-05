from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tgmate.models import Task
from .base import BaseController


class TaskController(BaseController):
    def __init__(self, engine: Engine, _session: Optional[Session] = None) -> None:
        super().__init__(engine, Task, _session)