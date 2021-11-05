from time import sleep
from telebot import TeleBot
from telebot import types
from typing import Dict, Callable
from .bot_reply import BotReply


class BotReplyForwarder(BotReply):
    def __init__(self, bot: TeleBot):
        handlers: Dict[str, Callable] = {
            '/start': self.__start
        }
        super().__init__(bot, handlers)
    
    def __start(self, message: types.Message):
        self._bot.send_message(message.chat.id, 'on start handler')

    def no_command_mode(self, msg: types.Message) -> None:
        if self._is_forwarded_message(msg):
            pass
            pass