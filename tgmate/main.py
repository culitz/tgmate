import sys
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from initialize import bot
from initialize import app
from threading import Thread
from datetime import date
from bot import CalendarReply, BotReplyForwarder

@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
            'text', 'location', 'contact', 'sticker'])
def on_base_commands(msg: Message):
    print('handler')

    forward_from = msg.forward_from is not None
    forward_date = msg.forward_date is not None

    markup = CalendarReply(bot, date.today())
    bot.send_message(msg.chat.id, f'handle {msg.text}')

@bot.message_handler(func=lambda message: True)
def foo(msg: Message):
    pass

#reply = BotReplyForwarder(bot)

def bot_pooling():
    while True:
        bot.polling(timeout=120)

def start_app():
    app.run()

print(str(sys.path))
bot_thread = Thread(target=bot_pooling)
app_thread = Thread(target=start_app)

bot_thread.start()
app_thread.start()
bot_thread.join()
app_thread.join()