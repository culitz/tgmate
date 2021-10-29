__author__ = 'ivan.koryshkin@gmail.com'
# Standart
import logging
from typing import Optional, Tuple
# Flask
from flask import Flask
from flask_admin import Admin
# Telegramb bot API
from telebot import TeleBot
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
# TgMate

from config import Config
from models import User, TgUser, Base, Message, Chat
from views import UserModelView
from views import TgUserView
from views import MessageView
from views import ChatView


log = logging.getLogger(__name__)
config = Config(log, DotEnv=True)

if config.check_env_vars() is False:
    log.error('Environment variables error')
    exit()

engine: Optional[Engine] = create_engine(config.get_db_url())
Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

bot = TeleBot(config.get_token()) 


def get_flask_apps() -> Tuple[Flask, Admin]:
    """
    Initializing Flask apps
    """
    app = Flask(__name__)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='tgmate', template_mode='bootstrap3')

    admin.add_view(UserModelView(User, db_session))
    admin.add_view(TgUserView(TgUser, db_session))
    admin.add_view(MessageView(Message, db_session))
    admin.add_view(ChatView(Chat, db_session))
    return app, admin

app, admin = get_flask_apps()