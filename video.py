import os
#os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from fer import FER
from fer import Video


class PlaylistMaker:
    def __init__(self, video_path):
        self.video_path = video_path

    def scan_emotions(self):
        # Добавляем из библиотеки детектор эмоций и указываем путь до видео, которое будем использовать

        emotion_detector = FER(mtcnn=True)
        video = Video(self.video_path)

        # Говорим программе проанализировать видео на эмоции

        result = video.analyze(emotion_detector, display=True)

        # Добавляем таблицу для определения эмоций на каждом кадре видео

        emotions_df = video.to_pandas(result)
        emotions_df.head()
        emo_dict = {'angry': round(emotions_df.angry.mean() * 10), 'happy': round(emotions_df.happy.mean() * 10), 'disgust': round(emotions_df.disgust.mean() * 10),
            'fear': round(emotions_df.fear.mean() * 10), 'neutral': round(emotions_df.neutral.mean() * 10), 'sad': round(emotions_df.sad.mean() * 10),
            'surprise': round(emotions_df.surprise.mean() * 10)}

        return emo_dict

    def make_playlist(self):
        emo_dict = dict(sorted(self.scan_emotions().items(), key=lambda item: item[1]))
        print(emo_dict)
        emos = list(emo_dict)
        song_list = []
        for i in range(len(emo_dict)):
            for j in range(emo_dict.get(emos[i])):
                if len(song_list) == 10:
                    break
                song_list.append(emos[i])
        if len(song_list) < 10:
            song_list.append(emos[-1])
        return song_list
