import geneticLib as GL

# создаем первичную нейронную сеть
net = GL.NN()  # создаем потомок класса
net.iCreate(4, [8], 1)  # инициализируем сеть
net.showNet()  # Отобразить нейронку

net.setDataset(1)
net = net.learnNet(net, 9)

for i in range(200):
    net = net.learnNet(net, 0)

net = net.learnNet(net, 9)