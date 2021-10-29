import os
import unittest
import string
from typing import List
from dotenv import load_dotenv
from telebot.types import Message, User, Chat
from tgmate.bot.bot_reply import BotReply



class TestBotReply(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()

    def test_command_name_whitelist(self):
        bot_reply = BotReply({})
        # Get all punctuation ASCII symbols 
        symbols: list = list(string.punctuation)
        # Removing right symbol from list
        symbols.remove('/')

        bad_commands: list = [f'{item}start' for item in symbols]
        status_list: list = []

        for command in bad_commands:
            is_ok: bool = bot_reply._check_command(command)
            status_list.append(not is_ok)
        
        all_true: bool = all(status_list)
        self.assertTrue(all_true)

    def test_check_handler_dict(self):
        # Create test handler
        def test_handler(message: dict):
            pass
        
        br_list: List[BotReply] = [
            BotReply({'/start': test_handler}),
            BotReply({'/start': None}),
            BotReply({'/start': 1}),
            BotReply({'/start': 'akdhak'}),
            BotReply({'&start': test_handler})
        ]

        count_true: int = 0
        count_false: int = 0

        for br in br_list:
            br._check_handlers()
            if br._is_handlers_correct:
                count_true += 1
            else:
                count_false += 1

        self.assertEqual(count_true, 1)
        self.assertEqual(count_false, 4)

    def test_handler_call(self):
        # Create test handler
        def test_handler(message: Message):
            message.text += '0'
        
        user = User(22, False, 'first_name')
        chat = Chat(464, 'type')
        msg = Message(1, user, 1231231, chat, 'dsa', {}, 'ajkdshkajsh')
        msg.text = '/start'

        br = BotReply({'/start': test_handler})
        br.on_message(msg)
        is_called: bool = msg.text == '/start0'
        self.assertTrue(is_called)
