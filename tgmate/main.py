from telebot.types import Message
from initialize import bot
from initialize import log

@bot.message_handler(content_types=['text'])
def on_base_commands(msg: Message):
    print('handler')
    bot.send_message(msg.chat.id, f'handle {msg.text}')

if __name__ == '__main__':
    log.info('[BOT] started')
    while True:
        bot.polling(timeout=120)