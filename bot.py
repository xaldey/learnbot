from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases = True)
    text = 'Привет {}'.format(emo)
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_text = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)

def send_rhino_picture(bot, update):
    rhino_list = glob('images/rhino*.jp*g')
    rhino_list = choice(rhino_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(rhino_list, 'rb'))


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('rhino', send_rhino_picture))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()
