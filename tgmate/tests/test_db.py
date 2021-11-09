from typing import Dict, List, Optional, Tuple, Callable
import unittest
import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import case
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import Query
from sqlalchemy.engine import Engine

from tgmate.config import Config
from tgmate.controller.task import TaskController
from tgmate.models import Base
from tgmate.models import Chat
from tgmate.models import Message
from tgmate.models import TgUser
from tgmate.models import User
from tgmate.models import Task

from tgmate.controller import UserController
from tgmate.controller import TgUserController
from tgmate.controller import MessageController
from tgmate.controller import ChatController
from tgmate.controller import BaseController


class TestBaseDB(unittest.TestCase):
    __TEST__ = False
    model_instance: Optional[Base] = None
    Model: Optional[Base] = None
    Controller: Optional[BaseController] = None

    _id: Optional[int] = None
    create_args = {}

    def setUp(self) -> None:
        config = Config(DotEnv=True, Test=True)
        db_url: str = config.get_db_url()
        self.engine: Engine = create_engine(db_url)
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        return super().setUp()
    
    @staticmethod
    def erase_table(model_type, session):
        query: Query = session.query(model_type).all()
        for q in query:
            session.delete(q)
        session.commit()

    def model_create(self) -> Tuple[bool, str]:
        self.erase_table(self.Model, self.session)
        try:
            self.model_instance = self.Model(**self.create_args)
            self.session.add(self.model_instance)
            self.session.commit()
            self._id = self.model_instance.id
            return True, self.get_name(self.model_create, '')
        except Exception as ex:
            return False, self.get_name(self.model_create, str(ex))
    
    def model_read(self) -> Tuple[bool, str]:
        try:
            query: Query = self.session.query(self.Model).filter(self.Model.id == self._id)
            return query.count() != 0, self.get_name(self.model_read, 'count() == 0')
        except Exception as ex:
            return False, self.get_name(self.model_read, str(ex))

    def model_delete(self):
        try:
            self.session.delete(self.model_instance)
            self.session.commit()
            count: int = self.session.query(self.Model).filter(self.Model.id == self._id).count()
            self.session.close()
            return count == 0, self.get_name(self.model_delete, 'count != 0') 
        except Exception as ex:
            return False, self.get_name(self.model_delete, str(ex))

    def controller_create(self) -> Tuple[bool, str]:
        try:
            model = self.Model(**self.create_args)
            controller = self.Controller(self.engine, self.session)
            is_created: bool = controller.create(model)
            self._id = model.id
            return is_created, self.get_name(self.controller_create, '')
        except Exception as ex:
            return False, self.get_name(self.controller_create, str(ex))

    def controller_read(self) -> bool:
        try:
            controller = self.Controller(self.engine, self.session)
            query: Query = controller.read(self.Model.id == self._id)
            is_created = True if query.count() != 0 else False
            return is_created, self.get_name(self.controller_read, '')
        except Exception as ex:
            return False, self.get_name(self.controller_read, str(ex))
    
    def controller_delete(self) -> bool:
        try:
            controller = self.Controller(self.engine, self.session)
            query: Query = controller.read(self.Model.id == self._id)
            model: Base = query.first()
            controller.delete(model)

            query: Query = controller.read(self.Model.id == self._id)
            is_created = False if query.count() == 0 else True
            return not is_created, self.get_name(self.controller_delete, '')

        except Exception as ex:
            return False, self.get_name(self.controller_delete, str(ex))

    def get_name(self, func: Callable, ex_msg: str) -> str:
        return f'[object: {self.__class__.__name__} func: {func.__name__}] {ex_msg}'

    def controller_is_none(self) -> Tuple[bool, str]:
        return False, f'[{self.Model.__class__.__name__}] controller not found!'
    
    def test(self):
        if self.__TEST__:
            res: List[Tuple[bool, str]] = []
            res.append(self.model_create())
            res.append(self.model_read())
            res.append(self.model_delete())

            if self.Controller is not None:
                res.append(self.controller_create())
                res.append(self.controller_read())
                res.append(self.controller_delete())
            else:
                res.append(self.controller_is_none())

            for tuple in res:
                self.assertTrue(tuple[0], msg=tuple[1])


class TestUserModel(TestBaseDB, unittest.TestCase):
    __TEST__ = True
    Model = User
    Controller = UserController
    create_args = {'login':'test-login', 'password':'test_pass', 'first_name':'f_name', 'last_name':'l_name'}


class TestTgUserModel(TestBaseDB, unittest.TestCase):
    __TEST__ = True
    Model = TgUser
    Controller = TgUserController
    create_args = {
            'tg_id': 54321,
            'is_bot': True,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'username': 'username',
            'language_code': None,
            'can_join_groups': None,
            'can_read_all_group_messages': None,
            'supports_inline_queries': None}

class TestMessageModel(TestBaseDB, unittest.TestCase):
    __TEST__ = True
    Model = Message
    Controller = MessageController
    create_args = {
            'message_id': 123123,
            'date': datetime.datetime.now(),
            'chat_id': 1}

class TestChatModel(TestBaseDB, unittest.TestCase):
    __TEST__ = True
    Model = Chat
    Controller = ChatController
    create_args = {'tg_id': 123123}

class TestTaskModel(TestBaseDB, unittest.TestCase):    
    __TEST__ = True
    Model = Task
    Controller = TaskController
    create_args = {
        'date': datetime.datetime.now(),
        'status': False,
        'author': 123
    }