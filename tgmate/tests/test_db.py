import os
from typing import Dict, List, Optional, Tuple
import unittest
import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import case
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import Query
from sqlalchemy.engine import Engine

from tgmate.config import Config
from tgmate.models import Base
from tgmate.models import Chat
from tgmate.models import Message
from tgmate.models import TgUser
from tgmate.models import User

from tgmate.controller import UserController
from tgmate.controller import TgUserController
from tgmate.controller import MessageController
from tgmate.controller import ChatController
from tgmate.controller import BaseController


class TestBaseModel(unittest.TestCase):
    __TEST__ = False
    Model = Base
    Controller = BaseController
    # create_args = {}
    model_instance: Optional[Base] = None
    _id: Optional[int] = None

    def setUp(self) -> None:
        load_dotenv()
        config = Config()
        config.set_host(os.getenv('TEST_DB_HOST'))
        config.set_passwd(os.getenv('TEST_DB_PASS'))
        config.set_port(os.getenv('TEST_DB_PORT'))
        config.set_user(os.getenv('TEST_DB_USER'))
        config.set_db_driver(os.getenv('TEST_DB_DRIVER'))
        config.set_db(os.getenv('TEST_DB_NAME'))

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

    def create(self) -> Tuple[bool, str]:
        self.erase_table(self.Model, self.session)
        case_name = '[CREATE CASE]'
        try:
            self.model_instance = self.Model(**self.create_args)
            self.session.add(self.model_instance)
            self.session.commit()
            self._id = self.model_instance.id
            return True, case_name
        except Exception as ex:
            return False, f'{case_name} {str(ex)}'
    
    def read(self) -> Tuple[bool, str]:
        case_name = '[READ CASE]'
        try:
            query: Query = self.session.query(self.Model).filter(self.Model.id == self._id)
            return query.count() != 0, f"{case_name} {query.count()} {self._id}"
        except Exception as ex:
            return False, f"{case_name} {str(ex)}"

    def delete(self):
        try:
            case_name = 'DELETE CASE'
            self.session.delete(self.model_instance)
            self.session.commit()
            count: int = self.session.query(self.Model).filter(self.Model.id == self._id).count()
            self.session.close()
            return count == 0, case_name 
        except Exception as ex:
            return False, f"{case_name} {str(ex)}"
    
    def test(self):
        if self.__TEST__:
            res: List[Tuple[bool, str]] = []
            res.append(self.create())
            res.append(self.read())
            res.append(self.delete())

            for tuple in res:
                self.assertTrue(tuple[0], msg=tuple[1])



class TestUserModel(TestBaseModel, unittest.TestCase):
    __TEST__ = True
    Model = User
    Controller = UserController
    create_args = {'login':'test-login', 'password':'test_pass', 'first_name':'f_name', 'last_name':'l_name'}


class TestTgUserModel(TestBaseModel, unittest.TestCase):
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

class TestMessageModel(TestBaseModel, unittest.TestCase):
    __TEST__ = True
    Model = Message
    Controller = MessageController
    create_args = {
            'message_id': 123123,
            'date': datetime.datetime.now(),
            'chat_id': 1}

class TestChatModel(TestBaseModel, unittest.TestCase):
    __TEST__ = True
    Model = Chat
    Controller = ChatController
    create_args = {'tg_id': 123123}    



class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        config = Config()
        config.set_host(os.getenv('TEST_DB_HOST'))
        config.set_passwd(os.getenv('TEST_DB_PASS'))
        config.set_port(os.getenv('TEST_DB_PORT'))
        config.set_user(os.getenv('TEST_DB_USER'))
        config.set_db_driver(os.getenv('TEST_DB_DRIVER'))
        config.set_db(os.getenv('TEST_DB_NAME'))

        db_url: str = config.get_db_url()
        self.engine: Engine = create_engine(db_url)

        Base.metadata.create_all(self.engine)
        return super().setUp()

    @staticmethod
    def erase_table(model_type, session):
        query: Query = session.query(model_type).all()
        for q in query:
            session.delete(q)
        session.commit()

    def test_controller_user(self):
        test_controller_login: str = 'ctl-test-user-login'
        test_pass: str = 'test pass'
        user = User(
            login=test_controller_login,
            password=test_pass,
            first_name='f_name',
            last_name='l_name'
        )
        with Session(self.engine) as session:
            self.erase_table(User, session)

            user_ctl = UserController(self.engine, session)

            # CRATE
            is_created: bool = user_ctl.create(user)
            self.assertTrue(is_created, "[CRATE] Create return True")

            # READ
            query: Query = user_ctl.read(User.login == test_controller_login)
            is_created = True if query.count() != 0 else False
            self.assertTrue(is_created, "[READ] Model was not read")

            user0: User = query.first()
            self.assertEqual(user0.id, user.id, "[READ] Models are different ")

            # UPDATE
            test_pass_new = test_pass * 2
            done: bool = user_ctl.update(User.login == test_controller_login, password=test_pass_new)
            self.assertTrue(done, "[UPDATE] Returning False")
            query: Query = user_ctl.read(User.login == test_controller_login)
            updated_model: User = query.first()
            self.assertEqual(updated_model.password, test_pass_new, '[UPDATE] Model was not updated')

            # Delete
            user_ctl.delete(user)
            query: Query = user_ctl.read(User.login == test_controller_login)
            is_created = False if query.count() == 0 else True
            self.assertFalse(is_created, "[DELETE] Model was not deleted")

    def test_controller_tg_user(self):
        test_tg_id = 222
        test_tg_user_username = 'username'
        tg_user = TgUser(
            tg_id=test_tg_id,
            is_bot=True,
            first_name='first_name',
            last_name='last_name',
            username=test_tg_user_username,
            language_code=None,
            can_join_groups=None,
            can_read_all_group_messages=None,
            supports_inline_queries=None
        )
        with Session(self.engine) as session:
            self.erase_table(TgUser, session)

            tg_user_ctl = TgUserController(self.engine, session)

            # CRATE
            is_created: bool = tg_user_ctl.create(tg_user)
            self.assertTrue(is_created, "[CRATE] Create return False")

            # READ
            query: Query = tg_user_ctl.read(TgUser.tg_id == test_tg_id)
            is_created = True if query.count() != 0 else False
            self.assertTrue(is_created, "[CRATE] Create return True")

            tg_user0: TgUser = query.first()
            self.assertEqual(tg_user0.id, tg_user.id, "[READ] Models are different ")

            #  UPDATE
            username_new = test_tg_user_username * 2
            done: bool = tg_user_ctl.update(TgUser.tg_id == test_tg_id, username=username_new)
            self.assertTrue(done, "[UPDATE] Returning False")
            query: Query = tg_user_ctl.read(TgUser.tg_id == test_tg_id)
            updated_model: TgUser = query.first()
            self.assertEqual(updated_model.username, username_new, '[UPDATE] Model was not updated')

            # Delete
            tg_user_ctl.delete(tg_user)

            query: Query = tg_user_ctl.read(TgUser.tg_id == test_tg_id)
            is_created = False if query.count() == 0 else True
            self.assertFalse(is_created, "[DELETE] Model was not deleted")

class TestControllerMessage(TestModel, unittest.TestCase):
    def test_controller_message(self):
        test_message_id = 125
        chat_id = 1
        msg = Message(
            message_id=test_message_id,
            date=datetime.datetime.now(),
            chat_id=chat_id
        )
        with Session(self.engine) as session:
            self.erase_table(Message, session)
            message_ctl = MessageController(self.engine, session)

            # CRATE
            is_created: bool = message_ctl.create(msg)
            self.assertTrue(is_created, "[CRATE] Create return True")

            # READ
            query: Query = message_ctl.read(Message.message_id == test_message_id)
            is_created = True if query.count() != 0 else False
            self.assertTrue(is_created, "READ")

            msg0: Message = query.first()
            self.assertEqual(msg0.id, msg.id, "[READ] Models are different ")

            #  UPDATE
            chat_id_new = chat_id * 2
            done: bool = message_ctl.update(Message.message_id == test_message_id, chat_id=chat_id_new)
            self.assertTrue(done, "[UPDATE] Returning False")
            query: Query = message_ctl.read(Message.message_id == test_message_id)
            updated_model: Message = query.first()
            self.assertEqual(updated_model.chat_id, chat_id_new, '[UPDATE] Model was not updated')

            # DELETE
            message_ctl.delete(msg)

            query: Query = message_ctl.read(Message.message_id == test_message_id)
            is_created = False if query.count() == 0 else True
            self.assertFalse(is_created, "[DELETE] Model was not deleted")


class TestControllerChat(TestModel, unittest.TestCase):
    def test_controller_chat(self):
        test_chat_id = 11256
        test_title = 'test title'
        chat = Chat(tg_id=test_chat_id, title=test_title)
        with Session(self.engine) as session:
            self.erase_table(User, session)

            chat_ctl = ChatController(self.engine, session)

            # CRATE
            is_created: bool = chat_ctl.create(chat)
            self.assertTrue(is_created, "[CRATE] Create return True")

            # READ
            query: Query = chat_ctl.read(Chat.tg_id == test_chat_id)
            is_created = True if query.count() != 0 else False
            self.assertTrue(is_created, "READ")

            chat0: Chat = query.first()
            self.assertEqual(chat0.id, chat.id, "[READ] Models are different")

            #  UPDATE
            title_new = test_title * 2
            done: bool = chat_ctl.update(Chat.tg_id == test_chat_id, title=title_new)
            self.assertTrue(done, "[UPDATE] Returning False")
            query: Query = chat_ctl.read(Chat.tg_id == test_chat_id)
            updated_model: Chat = query.first()
            self.assertEqual(updated_model.title, title_new, '[UPDATE] Model was not updated')

            # UPDATE MULTIPLE
            test_firstname = 'fn'
            test_last_name = 'ln'
            done: bool = chat_ctl.update(
                Chat.tg_id == test_chat_id,
                title=test_title,
                first_name=test_firstname,
                last_name=test_last_name
            )
            self.assertTrue(done, "[UPDATE MULTIPLE ATTRIBUTES] Returning False")
            query: Query = chat_ctl.read(Chat.tg_id == test_chat_id)
            updated_model: Chat = query.first()
            self.assertEqual(updated_model.title, test_title,
                             '[UPDATE MULTIPLE ATTRIBUTES] Model was not updated (title)')

            self.assertEqual(updated_model.first_name, test_firstname,
                             '[UPDATE MULTIPLE ATTRIBUTES] Model was not updated (test_firstname)')

            self.assertEqual(updated_model.last_name, test_last_name,
                             '[UPDATE MULTIPLE ATTRIBUTES] Model was not updated (last_name)')

            # DELETE
            chat_ctl.delete(chat)

            query: Query = chat_ctl.read(Chat.tg_id == test_chat_id)
            is_created = False if query.count() == 0 else True
            self.assertFalse(is_created, "[DELETE] Model was not deleted")
