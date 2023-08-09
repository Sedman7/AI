#=====================================================================================================
# за основу взяты примеры распознования рукописных цифр из MNIST
# и добавлена возможность рисовать мышкой цифру с возможностью ее разпознать
#
# после обучения точность распознаваний собственных изображений mnist - x_test очень
# высокая, около 98%, однако точность распознования цифр нарисованных мышкой была очень
# низкая, около 50-60% - возможно из-за того что рукописные цифры ручкой сильно отличаются от
# цифр написанных "мышкой"

# программа была доработана процедурой re_img - которая образала пустое пространство вокруг
# цифры, таким образом был обработан весь обучающий дата-сет и обрабатываются нарисованные
# пользователем цифры, благодаря чему точность распознования "художеств" пользователя
# выросла примерно до 90%
#=====================================================================================================

import numpy as np
from tensorflow.keras.datasets import mnist     #библиотека рукописных цифр от tensorflow
import matplotlib.pyplot as plt
import keras as k
import tkinter as tk
from PIL import Image, ImageOps, ImageTk

# процедура обрезки "пустоты" по краям изображения и растягивания того что осталось до исходных 28*28 точек
def re_img(img):
    image = Image.fromarray(img)
    t = img

    # уровень цвета учитываемых пикселей 0-255
    dark_lvl = 200

    tmax = np.amax(t, axis=1)   # формируем точки обрезки по X
    bx = 0
    ex = 28
    for i in range(28):
        if tmax[i] < dark_lvl and i < 10:
            bx += 1
        if tmax[i] < dark_lvl and i > 18:
            ex -= 1

    tmax = np.amax(t, axis=0)   # формируем точки обрезки по Y
    by = 0
    ey = 28
    for i in range(28):
        if tmax[i] < dark_lvl and i < 10:
            by += 1
        if tmax[i] < dark_lvl and i > 18:
            ey -= 1

    # режем
    i_crop = image.crop((by, bx, ey, ex))
    i_crop = i_crop.convert("L").resize((28, 28))

    return np.array(i_crop)

(x_train, y_train), (x_test,y_test) = mnist.load_data()  #загружаем изображения из mnist

#=====================================================================================================
# процесс обработки 60 000 изображений довольно длительный, по этому это сделали один раз
# обучили модель и сохранили данные о весах в файл, теперь просто идет подгрузка конфигурации весов
#=====================================================================================================
# z=0
# for i in range(len(x_train)):
#     x_train[i] = re_img(x_train[i])
#     z += 1
#     if z > 1000:
#         print(i)
#         z=0
    # os.system('clear')

# plt.imshow(x_train[7], cmap=plt.cm.binary)
# plt.show()

# # изменение размера изображений
# x_train14 = np.zeros((60000, 14, 14))
# for i in range(len(x_train)):
#     image = Image.fromarray(x_train[i])
#     x_train14[i] = image.convert("L").resize((14, 14))
#======================================================================================================

#нормализация данных - т.е. делаем так чтобы все значения были от 0 до 1
# x_train14 = x_train14/255
x_train = x_train/255
x_test = x_test/255

y_train_cat = k.utils.to_categorical(y_train, 10)
y_test_cat = k.utils.to_categorical(y_test, 10)

# создаем модель нейронной сети
# 1-й слой - Flaten - преобразование картинки в массив (двумерного массива в одномерный)
# 2-й 128 нейронов скрытого слоя и 3-й 10 нейронов выходного слоя
model = k.Sequential([
    k.layers.Flatten(input_shape=(28, 28, 1)),
    k.layers.Dense(128, activation='relu'),
    k.layers.Dense(10, activation='softmax')  # в задачах классификации лучшая функция активации softmax
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',  # в задачах классификации лучшая оценка потерь - categorical_entropy
              metrics=['accuracy'])

# обучили модель и сохранили данные о весах в файл, теперь просто идет подгрузка конфигурации весов
# history = model.fit(x_train, y_train_cat, batch_size=512, epochs=20, validation_split=0.2)
# model.save('digits.h5')

#загружаем сохраненные веса
model=k.models.load_model('digits.h5')

#создаем графический интерфейс
window = tk.Tk()
window.title("GUI вместе с tkinter")
window.geometry('300x350')

lbl = tk.Label(text="---")  #вывод результата распознования
lbl.grid(row=0, column=3, columnspan=3, pady=5)
#
# canvas = tk.Canvas(window, width=50, height=50, bg="white")

canv_s = tk.Canvas(window, width=28, height=28, bg="white")                   #
canv_s.grid(row=1, column=3, columnspan=3, pady=5)
# Отображаем изображение на холсте
# canv_s.create_image(200, 200, image=photo)

def recognize():
    print("Hello")
    canvas.postscript(file='my_draw.ps', colormode='gray')
    img = Image.open("my_draw.ps")
    img = ImageOps.invert(img.convert("L").resize((28, 28)))
    # img = ImageOps.invert(img)
    image = np.array(img)
    image = re_img(image)   # обрезаем пустоту

    image = image / 255

    # plt.imshow(photo, cmap=plt.cm.binary)
    # plt.show()

    x = np.expand_dims(image, axis=0)   # на вход ожидается подача данных вида 28х28х1 по этому к x_test Добавляем axis=0

    res = model.predict(x)              # получаем предсказание сети
    res = np.round(res*100, 0)          # переводим в %

    # отображаем в консоли все вероятности
    for i in range(res.shape[1]):
        print(str(i), ' - ', str(res[0, i]), '%')

    #выводим в консоль и на форму распознанную цифру
    print(f"Numeric: {np.argmax(res)}")
    lbl.configure(text=f"Numeric: {np.argmax(res)}")

    # plt.imshow(image, cmap=plt.cm.binary)
    # plt.show()

def save_digit(d):
    canvas.postscript(file='my_draw.ps', colormode='gray')
    img = Image.open("my_draw.ps")
    # img.show()
    sn = 'nums/'+str(d)+'/'+str(d)+'digit.png'

    # Обрезка белого пространства
    # Преобразование изображения в массив NumPy
    image_array = np.array(img)
    print(image_array)

    trimmed_image = re_img(image_array)
    image = Image.fromarray(trimmed_image)

    image.save(sn, "png")

    print(d)
    return 0

canvas = tk.Canvas(window, width=150, height=150, bg="white")                   # создали канву для рисования
canvas.grid(row=2, column=2, columnspan=6, pady=5)

btn = tk.Button(window, text="Распознать", command=recognize)                   # создали кнопки "распознать"
clr = tk.Button(window, text='Очистить', command=lambda: canvas.delete("all"))  # и "очистить"
btn.grid(row=3, column=2, columnspan=6, pady=5)
clr.grid(row=4, column=2, columnspan=6, pady=5)

btn0 = tk.Button(window, text="0", command=lambda: save_digit(0))
btn1 = tk.Button(window, text="1", command=lambda: save_digit(1))
btn2 = tk.Button(window, text="2", command=lambda: save_digit(2))
btn3 = tk.Button(window, text="3", command=lambda: save_digit(3))
btn4 = tk.Button(window, text="4", command=lambda: save_digit(4))
btn5 = tk.Button(window, text="5", command=lambda: save_digit(5))
btn6 = tk.Button(window, text="6", command=lambda: save_digit(6))
btn7 = tk.Button(window, text="7", command=lambda: save_digit(7))
btn8 = tk.Button(window, text="8", command=lambda: save_digit(8))
btn9 = tk.Button(window, text="9", command=lambda: save_digit(9))
btn0.grid(row=5, column=0, padx=5, pady=5)
btn1.grid(row=5, column=1, padx=5)
btn2.grid(row=5, column=2, padx=5)
btn3.grid(row=5, column=3, padx=5)
btn4.grid(row=5, column=4, padx=5)
btn5.grid(row=5, column=5, padx=5)
btn6.grid(row=5, column=6, padx=5)
btn7.grid(row=5, column=7, padx=5)
btn8.grid(row=5, column=8, padx=5)
btn9.grid(row=5, column=9, padx=5)

# процедура рисования
def draw(event):
    # рисуем линию на холсте
    x1, y1 = (event.x - 5), (event.y - 5)
    x2, y2 = (event.x + 5), (event.y + 5)
    canvas.create_oval(x1, y1, x2, y2, outline='#000000', fill="#000000")

# привязываем обработчики событий
canvas.bind("<B1-Motion>", draw)

window.mainloop()   # поехали...