# dice 	Dice 	Optional. Message is a dice with random value
# game 	Game 	Optional. Message is a game, information about the game. More about games »
# poll 	Poll 	Optional. Message is a native poll, information about the poll
# venue 	Venue 	Optional. Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set
# location 	Location 	Optional. Message is a shared location, information about the location
# new_chat_members 	Array of User 	Optional. New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)
# left_chat_member 	User 	Optional. A member was removed from the group, information about them (this member may be the bot itself)
# new_chat_title 	String 	Optional. A chat title was changed to this value
# new_chat_photo 	Array of PhotoSize 	Optional. A chat photo was change to this value
# delete_chat_photo 	True 	Optional. Service message: the chat photo was deleted
# group_chat_created 	True 	Optional. Service message: the group has been created
# supergroup_chat_created 	True 	Optional. Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
# channel_chat_created 	True 	Optional. Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
# message_auto_delete_timer_changed 	MessageAutoDeleteTimerChanged 	Optional. Service message: auto-delete timer settings changed in the chat
# migrate_to_chat_id 	Integer 	Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
# migrate_from_chat_id 	Integer 	Optional. The supergroup has been migrated from a group with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
# pinned_message 	Message 	Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it is itself a reply.
# invoice 	Invoice 	Optional. Message is an invoice for a payment, information about the invoice. More about payments »
# successful_payment 	SuccessfulPayment 	Optional. Message is a service message about a successful payment, information about the payment. More about payments »
# connected_website 	String 	Optional. The domain name of the website on which the user has logged in. More about Telegram Login »
# passport_data 	PassportData 	Optional. Telegram Passport data
# proximity_alert_triggered 	ProximityAlertTriggered 	Optional. Service message. A user in the chat triggered another user's proximity alert while sharing Live Location.
# voice_chat_scheduled 	VoiceChatScheduled 	Optional. Service message: voice chat scheduled
# voice_chat_started 	VoiceChatStarted 	Optional. Service message: voice chat started
# voice_chat_ended 	VoiceChatEnded 	Optional. Service message: voice chat ended
# voice_chat_participants_invited 	VoiceChatParticipantsInvited 	Optional. Service message: new participants invited to a voice chat
# reply_markup 	InlineKeyboardMarkup 	Optional. Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons.
__author__ = 'ivan.koryshkin@gmail.com'

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from tgmate.models import Base
from tgmate.config import TABLENAME_MESSAGE


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
    # Message is a shared contact, information about the contact
    # contact = Column()
    # dice = Column()
    # game = Column()
    # poll = Column()
    # venue = Column()
    # location = Column()
    # new_chat_members = Column()
    # left_chat_member = Column()
    # new_chat_title = Column()
    # new_chat_photo = Column()
    # delete_chat_photo = Column()
    # group_chat_created = Column()
    # supergroup_chat_created = Column()
    # channel_chat_created = Column()
    # message_auto_delete_timer_changed = Column()
    # migrate_to_chat_id = Column()
    # migrate_from_chat_id = Column()
    # pinned_message = Column()
    # invoice = Column()
    # successful_payment = Column()
    # connected_website = Column()
    # passport_data = Column()
    # proximity_alert_triggered = Column()
    # voice_chat_scheduled = Column()
    # voice_chat_started = Column()
    # voice_chat_ended = Column()
    # voice_chat_participants_invited = Column()
    # reply_markup = Column()
