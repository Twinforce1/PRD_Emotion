import telebot
from telebot import types  # для указания типов
from ya_music import YaMusic, PlaylistIDs, convert_to_id
from video import PlaylistMaker
from emo import PlaylistCreator
import os

bot = telebot.TeleBot('6576799018:AAEc7sN9LskdEWqt9h8-k819UU1K8LioUSY')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот для подбора музыкального плейлиста по твоему настроению. Отправь мне своё фото или видео (не более 5 секунд) и я скажу, что тебе нужно.".format(
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
    file_name = '../uploaded_photo.jpg'  # Имя файла, куда сохранить фотографию
    with open(file_name, 'wb') as f:
        f.write(file)
    with open('video.mp4', 'rb') as video_note_file:
        bot.send_video_note(message.chat.id, video_note_file)

    # Получаем слово из нейронки
    playlist_creator = PlaylistCreator(file_name)
    send_songs(playlist_creator, message)


@bot.message_handler(content_types=['video'])
def handle_video(message):
    # Получаем информацию о видео
    video = message.video
    file_id = video.file_id
    file_info = bot.get_file(file_id)

    # Создаем имя файла для сохранения видео
    file_name = f"uploaded_video.mp4"

    # Загружаем видео
    file = bot.download_file(file_info.file_path)

    # Сохраняем видео на сервере
    with open(file_name, 'wb') as f:
        f.write(file)
    with open('video.mp4', 'rb') as video_note_file:
        bot.send_video_note(message.chat.id, video_note_file)

    playlist_creator = PlaylistMaker(file_name)
    send_songs(playlist_creator, message)


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

    with open('video.mp4', 'rb') as video_note_file:
        bot.send_video_note(message.chat.id, video_note_file)

    playlist_creator = PlaylistMaker(file_name)
    send_songs(playlist_creator, message)
    # Удаляем сохраненное круглое видео
    os.remove(file_name)


def send_songs(playlist_creator, message):
    folder_list = playlist_creator.make_playlist()
    bot.send_message(message.chat.id, 'Плейлист обрабатывается, пожалуйста подождите')
    ya_downloader = YaMusic()
    # скачиваем песни по списку
    for folder in folder_list:
        playlist = convert_to_id(folder=folder)
        title = ya_downloader.download_track(playlist=playlist)
        print(title)
        with open(title, 'rb') as song:
            bot.send_audio(message.chat.id, song)
        os.remove(title)
    ya_downloader.clear()
    os.remove('uploaded_video.mp4')
    os.remove('data.csv')
    os.remove('output/uploaded_video_output.mp4')
    os.remove('output/images.zip')
    print('песни отправлены')


print('Бот включен')
bot.polling(none_stop=True)
