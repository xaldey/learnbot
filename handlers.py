from glob import glob
import logging
import os
from random import choice

from utils import get_keyboard, get_user_emo, is_rhino

def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {}'.format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Привет {} {}! Ты написал: {}".format(update.message.chat.first_name, emo, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_rhino_picture(bot, update, user_data):
    rhino_list = glob('images/rhino*.jp*g')
    rhino_pic = choice(rhino_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(rhino_pic, 'rb'))

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(emo), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def check_user_photo(bot, update, user_data):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    print(filename)
    photo_file.download(filename)
    if is_rhino(filename):
        update.message.reply_text("Обнаружен носорог! Добавляю в библиотеку!")
        new_filename = os.path.join('images', 'rhino_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        update.message.reply_text("Алярм! Носорога на фото не найдено!")
        os.remove(filename)  