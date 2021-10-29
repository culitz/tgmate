__author__ = 'ivan.koryshkin@gmail.com'

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from .base import Base
from tgmate.config import TABLENAME_CHAT


class Chat(Base):
    __tablename__ = TABLENAME_CHAT
    
    id = Column(Integer, primary_key=True)
    # Unique identifier for this chat. This number may have more than 32 significant bits and some programming 
    # languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, 
    # so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    tg_id = Column(Integer, nullable=True)
    # Type of chat, can be either “private”, “group”, “supergroup” or “channel”
    type = Column(String, nullable=True)
    # Title, for supergroups, channels and group chats
    title = Column(String, nullable=True)
    # Username, for private chats, supergroups and channels if available
    username = Column(String, nullable=True)
    # First name of the other party in a private chat
    first_name = Column(String, nullable=True)
    # Last name of the other party in a private chat
    last_name = Column(String, nullable=True)
    # Chat photo. Returned only in getChat.
    photo_id = Column(Integer, nullable=True)
    # Bio of the other party in a private chat.
    bio = Column(String, nullable=True)
    # Description, for groups, supergroups and channel chats
    description = Column(String, nullable=True)
    # Primary invite link, for groups, supergroups and channel chats.
    invite_link = Column(String, nullable=True)
    # The most recent pinned message (by sending date).
    pinned_message_id = Column(String, nullable=True)
    # Default chat member permissions, for groups and supergroups.
    permissions_id = Column(Integer, nullable=True)
    # For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user.
    slow_mode_delay = Column(Integer, nullable=True)
    # The time after which all messages sent to the chat will be automatically deleted; in seconds.
    message_auto_delete_time = Column(Integer, nullable=True)
    # For supergroups, name of group sticker set.
    sticker_set_name = Column(String, nullable=True)
    # True, if the bot can change the group sticker set.
    can_set_sticker_set = Column(Boolean, nullable=True)
    # Unique identifier for the linked chat, i.e. the discussion group identifier for a channel and vice versa; 
    # for supergroups and channel chats. This identifier may be greater than 32 bits and some programming 
    # languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 
    # 64 bit integer or double-precision float type are safe for storing this identifier.
    linked_chat_id = Column(Integer, nullable=True)
    # For supergroups, the location to which the supergroup is connected.
    location_id = Column(Integer, nullable=True)

    def __repr__(self):
        return str({
            'id': self.id,
            'tg_id': self.tg_id,
            'type': self.type,
            'title': self.title,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo_id': self.photo_id,
            'bio': self.bio,
            'description': self.description,
            'invite_link': self.invite_link,
            'pinned_message_id': self.pinned_message_id,
            'permissions_id': self.permissions_id,
            'slow_mode_delay': self.slow_mode_delay,
            'message_auto_delete_time': self.message_auto_delete_time,
            'sticker_set_name': self.sticker_set_name,
            'can_set_sticker_set': self.can_set_sticker_set,
            'linked_chat_id': self.linked_chat_id,
            'location_id': self.location_id,
        })