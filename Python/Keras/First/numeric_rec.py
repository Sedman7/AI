import numpy as np
from tensorflow.keras.datasets import mnist     #библиотека рукописных цифр от tensorflow
import matplotlib.pyplot as plt
import keras as k

(x_train, y_train), (x_test,y_test) = mnist.load_data()  #загружаем изображения из mnist

#нормализация данных - т.е. делаем так чтобы все значения были от 0 до 1
x_train = x_train/255
x_test = x_test/255

y_train_cat = k.utils.to_categorical(y_train, 10)
y_test_cat = k.utils.to_categorical(y_test, 10)

#k.Flatten(input_shape(28,28,1))  #преобразует массив 28х28х1 в входящий массив из 784 элементов

# plt.figure(figsize=(10,5))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.imshow(x_train[i], cmap=plt.cm.binary)

#plt.show()

#создаем модель нейронной сети
# 1-й слой - Flaten - преобразование картинки в массив (двумерного массива в одномерный)
# 2-й 128 нейронов скрытого слоя и 3-й 10 нейронов выходного слоя
model = k.Sequential([
    k.layers.Flatten(input_shape=(28, 28, 1)),
    k.layers.Dense(128, activation='relu'),
    k.layers.Dense(10, activation='softmax')  # в задачах классификации лучшая функция активации softmax
])

#print(model.summary(()))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',  # в задачах классификации лучшая оценка потерь - categorical_entropy
              metrics=['accuracy'])

history = model.fit(x_train, y_train_cat, batch_size=32, epochs=5, validation_split=0.2)

model.evaluate(x_test, y_test_cat)

n = 1

while n > 0:

    n = int(input("ВВедите номер картинки (0-выход): "))

    x = np.expand_dims(x_test[n], axis=0)  #на вход ожидается подача данных вида 28х28х1 по этому к x_test Добавляем axis=0

    res = model.predict(x)
    print(res)
    print(f"Numeric: {np.argmax(res)}")

    plt.imshow(x_test[n], cmap=plt.cm.binary)
    plt.show()