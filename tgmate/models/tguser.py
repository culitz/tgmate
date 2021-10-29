__author__ = 'ivan.koryshkin@gmail.com'

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from config import TABLENAME_TGUSER
from .base import Base

class TgUser(Base):
    __tablename__ = TABLENAME_TGUSER
    id = Column(Integer, primary_key=True)
    # Unique identifier for this user or bot. This number may have more than 32 significant bits 
    # and some programming languages may have difficulty/silent defects in interpreting it. But 
    # it has at most 52 significant bits, so a 64-bit integer or double-precision float type are 
    # safe for storing this identifier.
    tg_id = Column(Integer)
    # True, if this user is a bot
    is_bot = Column(Boolean)
    # User's or bot's first name
    first_name = Column(String)
    # User's or bot's last name
    last_name = Column(String, nullable=True)
    # User's or bot's username
    username = Column(String, nullable=True)
    # IETF language tag of the user's language
    language_code = Column(String, nullable=True)
    # True, if the bot can be invited to groups.
    can_join_groups = Column(Boolean, nullable=True)
    # True, if privacy mode is disabled for the bot.
    can_read_all_group_messages = Column(Boolean, nullable=True)
    # True, if the bot supports inline queries.
    supports_inline_queries = Column(Boolean, nullable=True)

    def __repr__(self):
        return str({
            'tg_id': self.tg_id,
            'is_bot': self.is_bot,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'language_code': self.language_code,
            'can_join_groups': self.can_join_groups,
            'can_read_all_group_messages': self.can_read_all_group_messages,
            'supports_inline_queries': self.supports_inline_queries
        })