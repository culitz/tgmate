import os
import logging
from typing import Optional
from threading import Thread
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from tgmate.config import Config


token: Optional[str] = None
engine: Optional[Engine] = None
config = Config()
log = logging.getLogger(__name__)

try:
    token = os.getenv('TOKEN')
    if config.check_env_vars() is False:
        log.error('Environment variables error')
        exit()
    engine = create_engine(config.get_db_url())
except Exception as ex:
    log.error(ex)
    exit()

if token is None:
    log.error('Token not found')
    exit()

if engine is None:
    log.error('Database connection failed')
    exit()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def foo():
    import time
    while True:
        time.sleep(1000)


flask_thread = Thread(target=app.run)
tgbot_thread = Thread(target=foo)

flask_thread.start()
tgbot_thread.start()
flask_thread.join()
tgbot_thread.join()
