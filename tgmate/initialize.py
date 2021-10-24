import logging
from typing import Optional
from dotenv.main import DotEnv
from flask import Flask
from telebot import TeleBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from config import Config


log = logging.getLogger(__name__)
config = Config(log, DotEnv=True)

if config.check_env_vars() is False:
    log.error('Environment variables error')
    exit()

engine: Optional[Engine] = create_engine(config.get_db_url())
app = Flask(__name__)
bot = TeleBot(config.get_token()) 
