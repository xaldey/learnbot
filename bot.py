import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from handlers import *
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY) #версия с прокси
    #mybot = Updater(settings.API_KEY) #версия без прокси

    logging.info('Бот запускается')

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('rhino', send_rhino_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать носорожку)$', send_rhino_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    #по другому никак хэндлер не прикручивался
    handler_photo = MessageHandler(Filters.photo, check_user_photo, pass_user_data=True)
    dp.add_handler(handler_photo)
    #dp.app_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__=="__main__":
    main()
