import cv2
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import os

print('Введи название папки')
folder = 'input'
mtcnn = MTCNN(image_size=48, margin=0, keep_all=True)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

#читаем файлы в папке
pictures = os.listdir(folder)
#обрезаем
for p in pictures:
    way = folder + '/' + p
    img = Image.open(way)
    save = 'cropped/' + p
    img_cropped = mtcnn(img, save_path=save)

pictures = os.listdir('cropped')
for p in pictures:
    way = 'cropped/' + p
    save = 'output/' + p
    im_gray = cv2.imread(way, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(save, im_gray)

print('Готово')