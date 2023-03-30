# кинуть файл my.py в content и потом подключить через импорт - пока это делать не нужно, весь код интегрирован сюда...
#import my
#my.Hi()

import random
import copy
#import os
#from IPython.display import clear_output

class NN:
#**************************************************************************************************************************#
#                 Инициализация, описания процедур для создания сети в рамках класс NN                                     #
#**************************************************************************************************************************#
  #набор данных для создания сети
  inValues = []  #входящие значения
  HL = []        #скрытые слои
  outValues = [] #выходные значения
  Links = []     #нейронные связи

  #наборы данных для обучения и проверки сети
  learnDataSet = [] #обучающая выборка состоит из набора разных inValues[]
  learnExpect = []  #ожидаемый результат для каждого набора входящих для обучения
  testDataSet = []  #контрольная выборка состоит из набора разных inValues[]
  testExpect = []   #ожидаемый результат для каждого набора входящих для теста

  valInValues = []  #входящие параметры - сюда кидаем или данные из valInValues или из testDataSet
  valExpect = []    #ожидаемый результат для каждого valInValues[] или testDataSet[]

  def __init__(self):
    self.inValues = []  #входящие значения
    self.HL = []        #скрытые слои
    self.outValues = [] #выходные значения
    self.Links = []     #нейронные связи

  #====================================== заполнение значением : ===========================================================
  #  процедура заполнения занных рандомным промежутком с заданной точностью
  #  precVal - точность знаков после запятой
  #========================================================================================================================
  def initVal(self,minVal,maxVal,precVal):
    pow = 10**precVal
    r = 0
    while r == 0:
      r = round(random.randrange(minVal*pow,maxVal*pow),precVal)/pow
    return r
  #-------------------------------------- End of initVal ------------------------------------------------------------------


  #====================================== подготовка, инициализация массивов: =============================================
  # процедура подготавливает (создает) нужные массивы и заполняет их рандомными данными
  # процедура на прямую не используется, используется внутри iCreate
  #========================================================================================================================
  def prepareArrays(self,inValuesP, NeronLayerP, outValuesP, minVal, maxVal, precVal):
    #формируем массив входящих значений
    for i in range(0,inValuesP):
      self.inValues.append(0.0)

    #формируем массив выходных значений
    for i in range(0,outValuesP):
      self.outValues.append(0.0)

    #формируем массив скрытых слоев
    for i in range(0,len(NeronLayerP)):
      tmpA = [] #обнуляем временный массив
      for j in range(0,NeronLayerP[i]):
        #tmpA.append(0.0) #заполняем нулями на указанное число раз
        tmpA.append(0.0)
      self.HL.append(tmpA)

    #формируем массив со связями
    Layers = 1 + len(NeronLayerP) #нужны веса от входных значений к слоям + от каждого скрытого слоя к следующему (последний к outValues)
    for i in range(0,Layers):
      #0 - веса от входных значений к слоям
      if i == 0:
        for j in range(0,inValuesP): #заполняем нулями на количество нейронов 1-го скрытого слоя
          tmpA = [] #обнуляем временный массив
          for k in range(0,NeronLayerP[0]): #заполняем нулями на количество нейронов 1-го скрытого слоя
            tmpA.append(self.initVal(minVal,maxVal,precVal))
          self.Links.append(tmpA)

      #последнее значение - веса от последнего скрытого слоя к outValues
      if i == Layers - 1:
        for j in range(0,NeronLayerP[i-1]): #заполняем нулями на количество нейронов последнего скрытого слоя
          tmpA = [] #обнуляем временный массив
          for k in range(0,outValuesP): #заполняем нулями на количество выходных значений
            tmpA.append(self.initVal(minVal,maxVal,precVal))
          self.Links.append(tmpA)

      #формируем массивы для всех скрытых слоев
      if i > 0 and i < Layers - 1:
        for j in range(0,NeronLayerP[i-1]): #заполняем нулями на количество нейронов последнего скрытого слоя
          tmpA = [] #обнуляем временный массив
          for k in range(0,NeronLayerP[i]): #заполняем нулями на количество выходных значений
            tmpA.append(self.initVal(minVal,maxVal,precVal))
          self.Links.append(tmpA)
  #-------------------------------------- End of prepareArrays ------------------------------------------------------------


  #====================================== процедура расчета: ==============================================================
  # процедура расчитывает всю сеть в 3 этапа: от входящих значений к скрытому слою; 2 внутри скрытых слоем; от скрытого слоя на выход
  #========================================================================================================================
  def netCalc(self):

    inCount = len(self.inValues) #Количество входящих параметров - надо для смещения в Links
    hidCount = 0            #Суммарное количество нейронов HL - надо для смещения в Links

    #просчитываем значения 1го скрытого слоя (от входящих значений к слою)
    for j in range(len(self.HL[0])): #для каждого HL[0][0]...HL[0][n] будем высчитывать значение
      res = 0
      for i in range(len(self.inValues)):             #берем каждый входящий параметр
        res = res + (self.inValues[i] * self.Links[i][j])  #и плюсуем к результату, вх. парам умноженный на вес
  #      print(Links[i][j])
      self.HL[0][j] = res

    #если больше 1 скрытого слоя то просчитываем все имеющиеся скрытые слои, кроме нулевого, его уже посчитали
    if len(self.HL) > 1:
      for k in range(len(self.HL)-1):
        for j in range(len(self.HL[k+1])): #для каждого HL[0][0]...HL[0][n] будем высчитывать значение
          res = 0
          for i in range(len(self.HL[k])):             #берем каждый входящий параметр
            res = res + (self.HL[k][i] * self.Links[i+inCount+hidCount][j])  #и плюсуем к результату, вх. парам умноженный на вес
  #          print(str(k),' ',str(HL[k][i]),' ',Links[i+inCount+hidCount][j])
          self.HL[k+1][j] = res

        #увеличиваем смещение в Links на количество нейронов предыдущего слоя
        hidCount = hidCount + len(self.HL[k])

    #print('всего линков: ' , str(len(self.Links)))
    #print('Количество нейронов последнего слоя: ', len(self.HL[len(self.HL)-1]))

    FirstLink = len(self.Links)-len(self.HL[len(self.HL)-1]) # высчитываем с какого слоя надо начинать просчет к выходным значениям

    #print('Нужно начать с линка: ', str(FirstLink))
    #print('И закончить линком: ',str(len(self.Links)-1))
    #print('Данные брать из последнего слоя: HL[', str(len(self.HL)-1),']')
    #print('Последний скрытый слой: ', self.HL[len(self.HL)-1])

    #просчитываем значения выходного слоя (от последнего скрытого к выходному)
    for j in range(len(self.outValues)): #для выходящего параметра будем высчитывать значение
      res = 0
      for i in range(len(self.HL[len(self.HL)-1])):             #берем каждый нейрон последнего слоя параметр
        res = res + (self.HL[len(self.HL)-1][i] * self.Links[i+FirstLink][j])  #и плюсуем к результату, нейрон умноженный на вес
        #print(Links[i+FirstLink][j])
      self.outValues[j] = res
  #-------------------------------------- End of netCalc ------------------------------------------------------------------


  #======================================  процедура отображения нейронной сети ===========================================
  # пока без параметров, просто отображаем массивы
  #========================================================================================================================
  def showNet(self):
    print('In Values: ', self.inValues)
    #print('Hiden layers:', HL)
    for i in range(len(self.Links)):
      print('Links layer ', str(i), ' :', self.Links[i])
    for i in range(len(self.HL)):
      print('Hidden Layer ', str(i), ' :', self.HL[i])
    print('Out Values:', self.outValues)
  #-------------------------------------- End of showNet ------------------------------------------------------------


  #======================================  процедура создания нейронной сети ==============================================
  #inValuesP - кол-во входящих параметров; #NeronLayerP - кол-во нейронов в [каждом скрытом слое]; #outValuesP - количество выходных параметров
  #задается сл. образом: iCreate(3,2,[3,5],2) - 3 входящих параметра, 2 скрытых слоя, размер первого 3, второго 5, 2 вых. параметра
  #========================================================================================================================
  def iCreate(self, inValuesP, NeronLayerP, outValuesP):

    #инициализируем датасеты
    self.initDataset()

    #подготавливаем массивы
    self.prepareArrays(inValuesP, NeronLayerP, outValuesP, -1,1,2)
  #-------------------------------------- End of iCreate -------------------------------------------------------------------

  #======================================  процедура корректировки весов Link у наследников ================================
  # веса корректируются на всех линках в пределах от -1 до +1
  # divVal - коэфициент деления для рандома, т.е. если divVal = 10 то корректировка -0.1 до +0.1 если divVal = 100 то -0.01 до +0.01 и тд
  #=========================================================================================================================
  def InhReLink(self,divVal):
    #print('всего линков: ' , str(len(self.Links)))
    for i in range(len(self.Links)):
      #print(' линк ', str(i),' ',str(len(self.Links[i])))
      for j in range(len(self.Links[i])):
        k = self.initVal(-1,1,10)
        self.Links[i][j] = self.Links[i][j] + k / divVal
  #-------------------------------------- End of InhReLink -----------------------------------------------------------------

  #======================================  функция рассчета ошибки =========================================================
  # функция вычитает expect - outValue, возвращает разницу
  #=========================================================================================================================
  def calcError(self,expect):
    res = abs(expect-self.outValues[0])
    return res
  #-------------------------------------- End of calcError -----------------------------------------------------------------

#**************************************************************************************************************************#
#                   Инициализация, описания процедур для обучения сети в рамках класс NN                                   #
#**************************************************************************************************************************#

  #======================================  функция обработки данных одним поколением =======================================
  # InhCount - количество потомков
  #=========================================================================================================================
  def oneGeneration(self,Net,InhCount):
    #создаем потомков нейронной сети (Inheriteds)
    Inh = []
    for i in range(0,InhCount):     #создаем InhCount потомков
      Inh.append(NN())              #создаем нового потомка
      Inh[i] = copy.deepcopy(Net)   #копируем потомку нашу сеть
      Inh[i].InhReLink(100)         #модифицируем для него линки
      Inh[i].netCalc()              #проводим расчет сети потомка
  #-------------------------------------- End of oneGeneration -------------------------------------------------------------


  #======================================  функция обучения сети ===========================================================
  # show = 0 - ничего не показывать  1 - показывать showNet() 2 показывать showNet() + комменты
  #=========================================================================================================================
  def learnNet(self,show):
    global net
    if show == 2 or show == 3 or show == 9:
      print('\n Начинаем обучение сети \nКоличество входящих значений: ', str(len(net.inValues)))
      print('Количество обучающих дата-сетов: ', str(len(self.valInValues)))   # + valExpect

    for i in range (len(self.valInValues)):   #перебираем весь обучающий дата-сет, проводя одну эпоху обучения
      net.inValues = self.valInValues[i]      #устанавливаем i-й датасет для обучения
      net.netCalc()
      Err = net.calcError(self.valExpect[i]) #высчитываем ошибку для i-го ожидаемого результата

      if show == 2 or show == 3 or show == 9:
        if self.valExpect[i] != 0: #вычисляем точность в %
          ErrPrc = round(net.outValues[0]*100/self.valExpect[i],2)
        else:
          ErrPrc = 0
        print(self.valInValues[i],' Выборка ',str(i+1),' из ',str(len(self.valInValues)),' Ответ:', str(net.outValues[0]),' ожидаем:', str(self.valExpect[i]),' Error = ', str(round(Err,2)),' (',str(ErrPrc),'%)')

      if show == 1 or show == 3:
        net.showNet()

      if show != 9: # 9 - просмотровый режим, в нем сеть не обучаем
        #создаем потомков нейронной сети (Inheriteds)
        Inh = []
        BestInh = -1
        for j in range(0,7):     #создаем InhCount потомков
          Inh.append(NN())              #создаем нового потомка
          Inh[j] = copy.deepcopy(net)   #копируем потомку нашу сеть
          Inh[j].InhReLink(100)         #модифицируем для него линки +/- 1/100
          Inh[j].netCalc()              #проводим расчет сети потомка
          InhErr = Inh[j].calcError(self.valExpect[i]) #расчет ошибки

          if InhErr < Err:
            BestInh = j                 #устанавливаем "Лучшим" № наследника если у него ошибка меньше чем у исходной сети или предыдущего
            Err = InhErr

          if show == 3:
            print(InhErr)

        if BestInh > -1:                      #если есть лучший потомок чем исходная сеть
          net = copy.deepcopy(Inh[BestInh])   #замещаем им нашу сеть

      if show == 3:
        print('Best = ', str(BestInh))
        print(' --- ')
  #-------------------------------------- End of learnNet ------------------------------------------------------------------

  #======================================  функция заполнения данными обучающей и тестовой =================================
  # learnDataSet = [] #обучающая выборка состоит из набора разных inValues[]
  # learnExpect = []  #ожидаемый результат для каждого набора входящих для обучения
  # testDataSet = []  #контрольная выборка состоит из набора разных inValues[]
  # testExpect = []   #ожидаемый результат для каждого набора входящих для теста
  #=========================================================================================================================
  def initDataset(self):
    # учим сеть сложению
    # #заполняем обущающий дата-сет
    # tmpA = [0,0,0,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(1)
    # tmpA = [0,0,1,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(1)
    # tmpA = [0,0,1,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(2)
    # tmpA = [0,1,0,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(1)
    # tmpA = [0,1,0,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(2)
    # tmpA = [0,1,1,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(2)
    # tmpA = [0,1,1,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(3)
    # tmpA = [1,1,1,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(3)
    # tmpA = [1,1,0,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(2)
    # tmpA = [1,1,1,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(4)

    # #заполняем тестовый дата-сет
    # tmpA = [3,1,0,9]; self.testDataSet.append(tmpA); self.testExpect.append(13)
    # tmpA = [0,1,7,2]; self.testDataSet.append(tmpA); self.testExpect.append(10)
    # tmpA = [9,1,9,5]; self.testDataSet.append(tmpA); self.testExpect.append(24)
    # tmpA = [0,0,0,0]; self.testDataSet.append(tmpA); self.testExpect.append(0)
    # tmpA = [9,9,9,9]; self.testDataSet.append(tmpA); self.testExpect.append(36)

    # учим сеть конвертации двоичная в десятичная
    # #заполняем обущающий дата-сет
    tmpA = [0,0,0,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(1)
    tmpA = [0,0,1,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(2)
    tmpA = [0,1,0,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(4)
    tmpA = [1,0,0,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(8)
    tmpA = [1,0,0,1]; self.learnDataSet.append(tmpA); self.learnExpect.append(9)
    tmpA = [0,1,1,0]; self.learnDataSet.append(tmpA); self.learnExpect.append(6)

    # #заполняем тестовый дата-сет
    tmpA = [0,1,1,1]; self.testDataSet.append(tmpA); self.testExpect.append(7)
    tmpA = [1,1,0,0]; self.testDataSet.append(tmpA); self.testExpect.append(14)
    tmpA = [1,0,1,0]; self.testDataSet.append(tmpA); self.testExpect.append(10)
    tmpA = [1,1,1,0]; self.testDataSet.append(tmpA); self.testExpect.append(18)

  #-------------------------------------- End of SetDataset ----------------------------------------------------------------

  #======================================  функция формирования обучаещего датасета ========================================
  # inData: 0 - обучающая выборка; 1 - контрольная выборка
  #=========================================================================================================================
  def setDataset(self,inData):
    self.valInValues = []
    self.valExpect = []

    if inData == 0:
      self.valInValues = self.learnDataSet
      self.valExpect = self.learnExpect

    if inData == 1:
      self.valInValues = self.testDataSet
      self.valExpect = self.testExpect
  #-------------------------------------- End of SetDataset ----------------------------------------------------------------


#**************************************************************************************************************************#
#                         Рабочая часть                                                                                    #
#**************************************************************************************************************************#

#создаем первичную нейронную сеть
net = NN()               #создаем потомок класса
net.iCreate(4,[8],1)    #инициализируем сеть
net.inValues = [1,1,1,1] #устанавливаем начальные значения входных нейронов
#net.netCalc()            #проводим расчет сети
net.showNet()            #Отобразить нейронку

#тут будем хранить конфигурацию изначальной нейронной сети для сравнения с результатом
fst = NN()
fst = copy.deepcopy(net)   #копируем нашу сеть

#формируем цикл для пошагового обучения сети
k=''
epoch = 0

while k != '999':

  #os.system('cls||clear')  #очистим консоль
  #clear_output()

  if k == '9':
    net.setDataset(1)
    net.learnNet(9)

  #обучаем сеть
  if k == '0':      #1 цикл обучения без отображения
    epoch = epoch + 1
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    net.learnNet(0)

  if k == '1':      #1 цикл обучения с отображением структуры
    epoch = epoch + 1
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    net.learnNet(1)

  if k == '2':      #1 цикл обучения с отображением комментариев
    epoch = epoch + 1
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    net.learnNet(2)

  if k == '3':      #1 цикл обучения с отображением структуры и комментариев
    epoch = epoch + 1
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    net.learnNet(3)

  if k == '10':      #10 циклов обучения без отображения
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    epoch = epoch + 10
    for i in range (0,10):
      net.learnNet(0)

  if k == '100':      #100 циклов обучения без отображения
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    epoch = epoch + 100
    for i in range (0,100):
      net.learnNet(0)

  if k == '1000':      #1000 циклов обучения без отображения
    net.setDataset(0) #вызываем процедуру формирования обучающего датасета
    epoch = epoch + 1000
    for i in range (0,100):
      net.learnNet(0)

  if k == '1008':     #1008 - показать сеть
    net.showNet()

  print('------------------------------------- Эпоха обучения: ',str(epoch),'-------------------------------------')
  k = input('цикл обучения: 0 - без инфо; 1 - структура; 2 - комменты; 3 - структура + комменты \n100, 1000 - 100 или 1000 циклов обучения в тихом режиме; 1008-показать сеть \n 9 - контроль \n999 - выход:')

