from telebot.types import Message
from initialize import bot
from initialize import log
from initialize import app
from threading import Thread


@bot.message_handler(content_types=['text'])
def on_base_commands(msg: Message):
    print('handler')
    bot.send_message(msg.chat.id, f'handle {msg.text}')

def bot_pooling():
    while True:
        bot.polling(timeout=120)

def start_app():
    app.run()

bot_thread = Thread(target=bot_pooling)
app_thread = Thread(target=start_app)

bot_thread.start()
app_thread.start()
bot_thread.join()
app_thread.join()