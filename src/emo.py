import cv2
from fer import FER


class PlaylistCreator:
    def __init__(self, image):
        self.image = image
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    def scan_emotions(self):
        input_image = cv2.imread(self.image)
        emotion_detector = FER()

        output_message = emotion_detector.detect_emotions(input_image)
        faces = len(output_message)
        if faces > 1 or faces == 0:
            return
        result = output_message[0].get('emotions')
        for i in range(len(self.emotions)):
            cur_emo = float(result.get(self.emotions[i]))
            result[self.emotions[i]] = int(round(cur_emo * 10))
        return result

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

