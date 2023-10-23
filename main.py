import telebot
from telebot import types  # для указание типов
import config
import random
import os

bot = telebot.TeleBot('6576799018:AAEc7sN9LskdEWqt9h8-k819UU1K8LioUSY')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отправить фотографию")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот для подбора музыкального плейлиста по твоему настроению. Отправь мне своё фото и я скажу, что тебе нужно.".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Отправить фотографию"):
        bot.send_message(message.chat.id, text="Жду фотографию твоего лица для определения настроения")

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    # Получение и сохранение фотографии
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    file_name = 'uploaded_photo.jpg'  # Имя файла, куда сохранить фотографию
    with open(file_name, 'wb') as f:
        f.write(file)

    # Отправка музыки

    music_directories = ['Грусть', 'Злость', 'Отвращение', 'Радость', 'Страх',
                         'Удивление']
    num_songs_to_send = 10
    # Получаем слово из нейронки
    text =

    for _ in range(num_songs_to_send):
        # Выбираем папку
        if "Грусть" in text:
            folder = 'Грусть'  # Замените 'folder1' на имя первой папки
        elif "Злость" in text:
            folder = 'Злость'  # Замените 'folder2' на имя второй папки
        elif "Отвращение" in text:
            folder = 'Отвращение'  # Замените 'folder3' на имя третьей папки
        elif "Радость" in text:
            folder = 'Радость'  # Замените 'folder4' на имя четвертой папки
        elif "Страх" in text:
            folder = 'Страх'  # Замените 'folder5' на имя пятой папки
        elif "Удивление" in text:
            folder = 'Удивление'  # Замените 'folder6' на имя шестой папки
        # Получаем список файлов в выбранной папке
        songs_in_directory = os.listdir(folder)
        if songs_in_directory:
            # Выбираем случайную песню из выбранной папки
            random_song = random.choice(songs_in_directory)
            song_path = os.path.join(folder, random_song)
            # Отправляем песню пользователю
            with open(song_path, 'rb') as song_file:
                bot.send_audio(message.chat.id, song_file)
        else:
            bot.send_message(message.chat.id, f"В папке {folder} нет песен.")


bot.polling(none_stop=True)