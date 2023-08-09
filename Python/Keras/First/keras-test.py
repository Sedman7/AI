from tkinter import *
from PIL import Image, ImageTk
import math

# Создаем окно приложения
root = Tk()

# Создаем холст размером 800x600 пикселей
canvas = Canvas(root, width=800, height=600)
canvas.pack()

# Создаем объект Image
image = Image.new("RGB", (800, 600), (0, 0, 0))

# Вычисляем координаты точек на изображении млечного пути
points = []
for x in range(800):
    y = int(300 + 100 * math.sin(x / 50))
    points.append((x, y))

# Заполняем пиксели изображения значениями цвета, соответствующими изображению млечного пути
for point in points:
    x, y = point
    image.putpixel((x, y), (255, 255, 255))

# Вычисляем положение космического корабля
ship_x = 400
ship_y = int(300 + 100 * math.sin(ship_x / 50))

# Заполняем пиксели изображения значениями цвета, соответствующими космическому кораблю
for x in range(ship_x - 10, ship_x + 11):
    for y in range(ship_y - 10, ship_y + 11):
        image.putpixel((x, y), (255, 0, 0))

# Создаем объект ImageTk.PhotoImage
photo = ImageTk.PhotoImage(image)

# Отображаем изображение на холсте
canvas.create_image(400, 300, image=photo)

# Запускаем главный цикл событий
root.mainloop()