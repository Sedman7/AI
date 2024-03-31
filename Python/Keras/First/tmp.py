from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import cv2
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers

# Загрузка изображения в градациях серого
image_gray = cv2.imread('imgs/cat1.png', cv2.IMREAD_GRAYSCALE)
# Преобразование изображения в массив NumPy
array_gray = np.array(image_gray)

# cv2.imshow('Images', image_gray)

image_gray = cv2.imread('imgs/fish1.png', cv2.IMREAD_GRAYSCALE)
array_gray2 = np.array(image_gray)

image_gray = cv2.imread('imgs/ulitka1.png', cv2.IMREAD_GRAYSCALE)
array_gray3 = np.array(image_gray)

X = np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]])

y = np.array([array_gray, array_gray2, array_gray3])

# Отображение массива в виде изображения
# plt.imshow(array_gray, cmap='gray')
# plt.axis('off')  # Отключение осей координат
# plt.show()


# Создание модели нейронной сети
# так как учим сеть конвертировать в десятичную из двоичной и считать функции активации оставляем линейными
# model = Sequential()
# model.add(Dense(200, input_dim=3))   # это значит 3 входящих нейрона, 4 нейрона на выходе
# model.add(Dense(2500))                # еще один слой - вход идет с прошлого слоя, на выходе 2500 нейрона
# Создание модели
model = keras.Sequential()

# Добавление слоев
model.add(layers.Dense(100, activation='relu', input_shape=(3,)))  # Скрытый слой с 100 нейронами
model.add(layers.Dense(50 * 50, activation='linear'))  # Выходной слой размером 50x50

# Изменение формы выхода
model.add(layers.Reshape((50, 50)))

# Вывод информации о модели
model.summary()

print('Compile model...')
# Компиляция модели
model.compile(loss='mean_squared_error', optimizer='sgd')

# Отображение массива в виде изображения
# plt.imshow(array_gray, cmap='gray')
# plt.axis('off')  # Отключение осей координат
# plt.show()

for i in range(10):

    print('Starting fit...')
    # Обучение модели verbose=0 - не отображать инфо об обучении, эпохах
    history = model.fit(X, y, epochs=50, verbose=1)

    X_test = np.array([[1, 0, 0]])

    predicted = model.predict(X_test)
    # print(predicted)

    # Преобразование предсказаний в изображение
    image = predicted.reshape((50, 50))

    cv2.imshow('Images', image)

    # Отображение массива в виде изображения
    # plt.imshow(image, cmap='gray')
    # plt.axis('off')  # Отключение осей координат
    # plt.show()