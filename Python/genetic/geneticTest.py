import geneticLib as GL

# создаем первичную нейронную сеть
net = GL.NN()  # создаем потомок класса
net.iCreate(4, [8], 1)  # инициализируем сеть
net.showNet()  # Отобразить нейронку

