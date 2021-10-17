from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query
from tgmate.models import Base


class BaseController:
    def __init__(self, engine: Engine, model_type: Base, _session: Optional[Session] = None) -> None:
        self._engine: Engine = engine
        self._model_type: Base = model_type
        self._session = _session if _session is not None else Session(self._engine)

    def create(self, model: Base) -> bool:
        """
        :param model: Model instance to create
        :type model: SQLAlchemy model
        """
        try:
            self._session.add(model)
            self._session.commit()
            return True
        except Exception as ex:
            return False

    def read(self, *args) -> Query:       
        return self._session.query(self._model_type).filter(*args)

    def update(self, *flt, **kwargs) -> bool:
        try:
            updated = False
            query: Query = self.read(*flt)
            for q in query:
                for key in kwargs:
                    if hasattr(q, key):
                        setattr(q, key, kwargs.get(key))
                        updated = True
            self._session.commit()
            return updated
        except Exception as ex:
            return False

    def delete(self, model_to_delete: Base) -> bool:       
        try:
            self._session.delete(model_to_delete)
            self._session.commit()
            return True
        except Exception as ex:
            return False
