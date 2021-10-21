import os
import collections
from typing import Optional, Callable, Dict
from telebot.types import Message


class BotReply:
    def __init__(self, handlers: Dict[str, Callable]):
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
        self._handlers: Dict[str, Callable] = handlers
        self._is_handlers_correct: Optional[bool] = None

    def on_message(self, message: Message) -> None:
        text: str = message.text.lower()
        if text not in self._handlers:
            return

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
            if fn is None or not isinstance(fn, collections.Callable):
                self._handlers_correct = False
                break

    @staticmethod
    def _check_command(command: str) -> bool:
        if len(command):
            return command[0] == '/'
        return False
