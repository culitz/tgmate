import os
from typing import Optional, Callable, Dict
from telebot.types import Message, User
from telebot import TeleBot
from initialize import bot



class BotReply:
    def __init__(self, bot: TeleBot, handlers: Dict[str, Callable] = {}):
        """
        BotReply constructor
        :key [any bot command name]:
            bot command start with '/'
            value must be a handler function

            example:
            def start_command_handler(message: types.Message) -> None:
                ...
            handlers = {'/start': start_command_handler}
            br = BotReply(handlers)
        """
        self.__content_types = ['audio', 'photo', 'voice', 'video', 'document', 
                                        'text', 'location', 'contact', 'sticker']
        self._handlers: Dict[str, Callable] = handlers
        self._is_handlers_correct: Optional[bool] = None
        self._command_list: list = list(handlers.keys())
        self._bot = bot
        self.__subscribe()

    def _on_message(self, message: Message) -> None:
        """
        On message handler
        :param message: incoming message
        :type message: types.Message
        """
        text: str = message.text.lower()
        if self._is_unknown_command(text):
            self.no_command_mode(message)
        else:
            handler_fn: Callable = self._handlers.get(text)
            handler_fn(message)

    def _check_handlers(self):
        """
        Checking the handler list
        All values in this list must be functions
        """
        if self._is_handlers_correct is not None:
            # if _is_handlers_correct is not none, it's means that the list has been checked earlier
            return

        for command in self._handlers:
            if not self._check_command(command):
                self._is_handlers_correct = False
                break

            fn: Optional[Callable] = self._handlers.get(command, None)
            if fn is None:
                self._is_handlers_correct = False
                break
            
            if not callable(fn):
                self._is_handlers_correct = False
                break
        
            self._is_handlers_correct = True

    @staticmethod
    def _check_command(command: str) -> bool:
        """
        Check that command format is correct.
        :param command: command string
        :type command: str
        """
        l: int = len(command)
        if l > 0:
            return command.startswith('/')
        return False

    @staticmethod
    def _is_forwarded_message(msg: Message) -> bool:
        return True if msg.forward_from is not None else False

    def no_command_mode(self, msg: Message) -> None:
        pass
    
    def _is_unknown_command(self, text: str) -> bool:
        return text not in self._handlers

    def __subscribe(self):
        @self._bot.message_handler(content_types=self.__content_types)
        def msg(msg: Message):
            self._on_message(msg)

    def __repr__(self) -> str:
        return f"BotReply [{self._is_handlers_correct}]"