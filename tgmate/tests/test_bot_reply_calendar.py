import unittest
import datetime
from telebot import types
from bot import CalendarReply
from .test_bot_reply import TestBotReply

class TestBotCalendarReply(TestBotReply, unittest.TestCase):
    
    def test_calendar_button(self):
        try:
            calendar = CalendarReply(self.bot, datetime.date.today())
            _ = calendar.to_json()
            self.assertTrue(True)
        except Exception as ex:
            self.assertTrue(False, msg=str(ex))

    def test_callback_navigate_prev(self):
        try:
            calendar = CalendarReply(self.bot, datetime.date.today())
            prev_meta: str = calendar._CalendarReply__navigation_prev_meta()
            u = types.User(1, False, 'test user')
            chat = types.Chat(464, 'type')
            q = types.CallbackQuery(1, u, prev_meta, chat)
            is_prev: bool = CalendarReply._CalendarReply__is_callback_prev(q)
            self.assertTrue(is_prev)
        except Exception as ex:
            self.assertTrue(False, msg=str(ex))

    def test_callback_navigate_prev(self):
        try:
            calendar = CalendarReply(self.bot, datetime.date.today())
            next_meta: str = calendar._CalendarReply__navigation_next_meta()
            u = types.User(1, False, 'test user')
            chat = types.Chat(464, 'type')
            q = types.CallbackQuery(1, u, next_meta, chat)
            is_next: bool = CalendarReply._CalendarReply__is_callback_next(q)
            self.assertTrue(is_next)
        except Exception as ex:
            self.assertTrue(False, msg=str(ex))
