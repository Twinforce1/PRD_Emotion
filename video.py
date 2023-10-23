import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from fer import FER
from fer import Video


class Emo_2007:
    def __init__(self):
        pass

    def video(self):
        # Добавляем из библиотеки детектор эмоций и указываем путь до видео, которое будем использовать

        emotion_detector = FER(mtcnn=True)

        path_to_video = "obrez.mov"

        video = Video(path_to_video)

        # Говорим программе проанализировать видео на эмоции

        result = video.analyze(emotion_detector, display=True)

        # Добавляем таблицу для определения эмоций на каждом кадре видео

        emotions_df = video.to_pandas(result)
        emotions_df.head()
        emo_dict = {'angry': round(emotions_df.angry.mean() * 10), 'happy': round(emotions_df.happy.mean() * 10), 'disgust': round(emotions_df.disgust.mean() * 10),
            'fear': round(emotions_df.fear.mean() * 10), 'neutral': round(emotions_df.neutral.mean() * 10), 'sad': round(emotions_df.sad.mean() * 10),
            'surprise': round(emotions_df.surprise.mean() * 10)}

        return emo_dict
