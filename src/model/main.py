import pandas as pd
import numpy as np
import tensorflow as tf
from keras.src.layers import BatchNormalization, Activation
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Загрузка данных из CSV файла
csv_file_path = "fer2013.csv"  # Укажите путь к вашему CSV файлу
data = pd.read_csv(csv_file_path)

# Разделение данных на признаки (X) и метки (y)
X = data['pixels'].apply(lambda x: np.fromstring(x, sep=' ', dtype=np.float32).reshape(48, 48, 1)).values.tolist()
X = np.array(X)
y = data['emotion'].values

# Преобразование меток классов в one-hot encoding
y_onehot = to_categorical(y, num_classes=7)  # Предполагается, что у вас 7 классов эмоций

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y_onehot, test_size=0.2, random_state=42)

# Нормализация данных
X_train = X_train / 255.0
X_test = X_test / 255.0


emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
num_classes = 7
width, height = 48, 48
num_epochs = 50
batch_size = 128
num_features = 64
model = Sequential()

model = Sequential()
model.add(Conv2D(2*2*num_features, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(2*num_features, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(7, activation='softmax'))

# Компиляция модели
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Обучение модели с записью истории точности
history = model.fit(X_train, y_train, epochs=num_epochs, batch_size=batch_size, validation_split=0.2)

# Оценка точности на тестовых данных
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {test_accuracy}')

# Сохранение модели
model.save("emotion_model.h5")

# Визуализация точности обучения
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
