import telebot
from telebot import types  # для указание типов
import config
import random
from video import PlaylistMaker
from emo import PlaylistCreator
import os

bot = telebot.TeleBot('6576799018:AAEc7sN9LskdEWqt9h8-k819UU1K8LioUSY')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот для подбора музыкального плейлиста по твоему настроению. Отправь мне своё фото или видео и я скажу, что тебе нужно.".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
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

    # Получаем слово из нейронки
    playlist_creator = PlaylistCreator(file_name)
    send_songs(playlist_creator)


@bot.message_handler(content_types=['video'])
def handle_video(message):
     # Получаем информацию о видео
    video = message.video
    file_id = video.file_id
    file_info = bot.get_file(file_id)

    # Создаем имя файла для сохранения видео
    file_name = f"{message.chat.id}_{file_id}.mp4"

    # Загружаем видео
    file = bot.download_file(file_info.file_path)

    # Сохраняем видео на сервере
    with open(file_name, 'wb') as f:
        f.write(file)

    playlist_creator = PlaylistMaker(file_name)
    send_songs(playlist_creator)


@bot.message_handler(content_types=['video_note'])
def handle_round_video(message):
    # Получаем информацию о видео
    video_note = message.video_note
    file_id = video_note.file_id
    file_info = bot.get_file(file_id)

    # Создаем имя файла для сохранения круглого видео
    file_name = f"{message.chat.id}_{file_id}.mp4"

    # Загружаем видео
    file = bot.download_file(file_info.file_path)

    # Сохраняем видео на сервере
    with open(file_name, 'wb') as f:
        f.write(file)

    # Отправляем круглое видео обратно в чат
    with open(file_name, 'rb') as round_video_file:
        bot.send_video_note(message.chat.id, round_video_file)

    playlist_creator = PlaylistMaker(file_name)
    send_songs(playlist_creator)
        # Удаляем сохраненное круглое видео
    os.remove(file_name)

def send_songs(playlist_creator):
    music_directories = ['sad', 'angry', 'disgust', 'happy', 'fear',
                         'surprise']
    folder_list = playlist_creator.make_playlist()
    sent_songs = set()

    for i in range(len(folder_list)):
        folder = folder_list[i]
        if folder_list[i] == 'neutral':
            folder = random.choice(music_directories)
        # Получаем список файлов в выбранной папке
        songs_in_directory = os.listdir(folder)
        if songs_in_directory:
            # Выбираем случайную песню из выбранной папки
            random_song = random.choice(songs_in_directory)
            while random_song in sent_songs:
                random_song = random.choice(songs_in_directory)
            sent_songs.add(random_song)
            song_path = os.path.join(folder, random_song)
            # Отправляем песню пользователю
            with open(song_path, 'rb') as song_file:
                bot.send_audio(message.chat.id, song_file)
        else:
            bot.send_message(message.chat.id, f"В папке {folder} нет песен.")




bot.polling(none_stop=True)