__author__ = 'ivan.koryshkin@gmail.com'

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from models import Base
from config import TABLENAME_MESSAGE


class Message(Base):
    __tablename__ = TABLENAME_MESSAGE
    
    id = Column(Integer, primary_key=True)
    # Unique message identifier inside this chat
    message_id = Column(Integer)
    # Sender, empty for messages sent to channels
    from_user_id = Column(Integer, nullable=True)
    # Sender of the message, sent on behalf of a chat. The channel itself for channel messages. 
    # The supergroup itself for messages from anonymous group administrators. The linked channel 
    # For messages automatically forwarded to the discussion group
    sender_chat_id = Column(Integer, nullable=True)
    # Date the message was sent in Unix time
    date = Column(DateTime)
    # Conversation the message belongs to
    chat_id = Column(Integer)
    # For forwarded messages, sender of the original message
    forward_from_id = Column(Integer, nullable=True)
    # For messages forwarded from channels or from anonymous administrators, information about the original sender chat
    forward_from_chat_id = Column(Integer, nullable=True)
    # For messages forwarded from channels, identifier of the original message in the channel
    forward_from_message_id = Column(Integer, nullable=True)
    # For messages forwarded from channels, signature of the post author if present
    forward_signature = Column(String, nullable=True)
    # Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages
    forward_sender_name = Column(String, nullable=True)
    # For forwarded messages, date the original message was sent in Unix time
    forward_date = Column(Integer, nullable=True)
    # For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
    reply_to_message_id = Column(String, nullable=True)
    # Bot through which the message was sent
    via_bot_id = Column(Integer, nullable=True)
    # Date the message was last edited in Unix time
    edit_date = Column(Integer, nullable=True)
    # The unique identifier of a media message group this message belongs to
    media_group_id = Column(String, nullable=True)
    # Signature of the post author for messages in channels, or the custom title of an anonymous group administrator
    author_signature = Column(String, nullable=True)
    # For text messages, the actual UTF-8 text of the message, 0-4096 characters
    text = Column(String, nullable=True)
    # For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
    entities = Column(String, nullable=True)
    # Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set
    animation_id = Column(String, nullable=True)
    # Message is an audio file, information about the file
    audio_id = Column(Integer, nullable=True)
    # Message is a general file, information about the file
    document_id = Column(Integer, nullable=True)
    # Message is a photo, available sizes of the photo
    photo = Column(Integer, nullable=True)
    # Message is a sticker, information about the sticker
    sticker = Column(Integer, nullable=True)
    # Message is a video, information about the video
    video_id = Column(Integer, nullable=True)
    # Message is a video note, information about the video message
    video_note_id = Column(Integer, nullable=True)
    # Message is a voice message, information about the file
    voice_id = Column(Integer, nullable=True)
    # Caption for the animation, audio, document, photo, video or voice, 0-1024 characters
    caption_id = Column(Integer, nullable=True)
    # For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
    caption_entities = Column(String, nullable=True)