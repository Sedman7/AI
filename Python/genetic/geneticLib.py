import random
import copy

class NN:
    # *****************************************************************************************************************#
    #                 Инициализация, описания процедур для создания сети в рамках класса NN                            #
    # *****************************************************************************************************************#
    # набор данных для создания сети
    inValues = []   # входящие значения
    HL = []         # скрытые слои
    outValues = []  # выходные значения
    Links = []      # нейронные связи

    # наборы данных для обучения и проверки сети
    learnDataSet = []  # обучающая выборка состоит из набора разных inValues[]
    testDataSet = []   # контрольная выборка состоит из набора разных inValues[]

    valInValues = []   # входящие параметры - сюда кидаем или данные из valInValues или из testDataSet
    valExpect = []     # ожидаемый результат для каждого valInValues[] или testDataSet[]

    def __init__(self):
        self.inValues = []   # входящие значения
        self.HL = []         # скрытые слои
        self.outValues = []  # выходные значения
        self.Links = []      # нейронные связи

    # ====================================== заполнение значением : ====================================================
    #  процедура заполнения данных рандомным промежутком с заданной точностью
    #  precVal - точность знаков после запятой
    # ==================================================================================================================
    def initVal(self, minVal, maxVal, precVal):
        pow = 10 ** precVal
        r = 0
        while r == 0:
            r = round(random.randrange(minVal * pow, maxVal * pow), precVal) / pow
        return r

    # -------------------------------------- End of initVal ------------------------------------------------------------

    # ====================================== подготовка, инициализация массивов: =======================================
    # процедура подготавливает (создает) нужные массивы и заполняет их рандомными данными
    # процедура на прямую не используется, используется внутри iCreate
    # ========================================================================================================================
    def prepareArrays(self, inValuesP, NeronLayerP, outValuesP, minVal, maxVal, precVal):
        # формируем массив входящих значений
        for i in range(0, inValuesP):
            self.inValues.append(0.0)

        # формируем массив выходных значений
        for i in range(0, outValuesP):
            self.outValues.append(0.0)

        # формируем массив скрытых слоев
        for i in range(0, len(NeronLayerP)):
            tmpA = []  # обнуляем временный массив
            for j in range(0, NeronLayerP[i]):
                # tmpA.append(0.0) # заполняем нулями на указанное число раз
                tmpA.append(0.0)
            self.HL.append(tmpA)

        # формируем массив со связями
        Layers = 1 + len(NeronLayerP)  # нужны веса от входных значений к слоям + от каждого скрытого слоя к следующему (последний к outValues)
        for i in range(0, Layers):
            # 0 - веса от входных значений к слоям
            if i == 0:
                for j in range(0, inValuesP):  # заполняем нулями на количество нейронов 1-го скрытого слоя
                    tmpA = []  # обнуляем временный массив
                    for k in range(0, NeronLayerP[0]):  # заполняем нулями на количество нейронов 1-го скрытого слоя
                        tmpA.append(self.initVal(minVal, maxVal, precVal))
                    self.Links.append(tmpA)

            # последнее значение - веса от последнего скрытого слоя к outValues
            if i == Layers - 1:
                for j in range(0,
                               NeronLayerP[i - 1]):  # заполняем нулями на количество нейронов последнего скрытого слоя
                    tmpA = []  # обнуляем временный массив
                    for k in range(0, outValuesP):  # заполняем нулями на количество выходных значений
                        tmpA.append(self.initVal(minVal, maxVal, precVal))
                    self.Links.append(tmpA)

            # формируем массивы для всех скрытых слоев
            if i > 0 and i < Layers - 1:
                for j in range(0, NeronLayerP[i - 1]):  # заполняем нулями на количество нейронов последнего скрытого слоя
                    tmpA = []  # обнуляем временный массив
                    for k in range(0, NeronLayerP[i]):  # заполняем нулями на количество выходных значений
                        tmpA.append(self.initVal(minVal, maxVal, precVal))
                    self.Links.append(tmpA)
    # -------------------------------------- End of prepareArrays -----------------------------------------------------

    # ====================================== процедура расчета: =======================================================
    # процедура расчитывает всю сеть в 3 этапа: от входящих значений к скрытому слою; 2 внутри скрытых слоем;
    # от скрытого слоя на выход
    # =================================================================================================================
    def netCalc(self):

        inCount = len(self.inValues)  # Количество входящих параметров - надо для смещения в Links
        hidCount = 0  # Суммарное количество нейронов HL - надо для смещения в Links

        # просчитываем значения 1го скрытого слоя (от входящих значений к слою)
        for j in range(len(self.HL[0])):  # для каждого HL[0][0]...HL[0][n] будем высчитывать значение
            res = 0
            for i in range(len(self.inValues)):  # берем каждый входящий параметр
                res = res + (self.inValues[i] * self.Links[i][j])  # и плюсуем к результату, вх. парам умноженный на вес
              # print(Links[i][j])
            self.HL[0][j] = res

        # если больше 1 скрытого слоя то просчитываем все имеющиеся скрытые слои, кроме нулевого, его уже посчитали
        if len(self.HL) > 1:
            for k in range(len(self.HL) - 1):
                for j in range(len(self.HL[k + 1])):  # для каждого HL[0][0]...HL[0][n] будем высчитывать значение
                    res = 0
                    for i in range(len(self.HL[k])):  # берем каждый входящий параметр
                        res = res + (self.HL[k][i] * self.Links[i + inCount + hidCount][j])  # и плюсуем к результату, вх. парам умноженный на вес
                      # print(str(k),' ',str(HL[k][i]),' ',Links[i+inCount+hidCount][j])
                    self.HL[k + 1][j] = res

                # увеличиваем смещение в Links на количество нейронов предыдущего слоя
                hidCount = hidCount + len(self.HL[k])

        # print('всего линков: ' , str(len(self.Links)))
        # print('Количество нейронов последнего слоя: ', len(self.HL[len(self.HL)-1]))

        FirstLink = len(self.Links) - len(
            self.HL[len(self.HL) - 1])  # высчитываем с какого слоя надо начинать просчет к выходным значениям

        # print('Нужно начать с линка: ', str(FirstLink))
        # print('И закончить линком: ',str(len(self.Links)-1))
        # print('Данные брать из последнего слоя: HL[', str(len(self.HL)-1),']')
        # print('Последний скрытый слой: ', self.HL[len(self.HL)-1])

        # просчитываем значения выходного слоя (от последнего скрытого к выходному)
        for j in range(len(self.outValues)):  # для выходящего параметра будем высчитывать значение
            res = 0
            for i in range(len(self.HL[len(self.HL) - 1])):  # берем каждый нейрон последнего слоя параметр
                res = res + (self.HL[len(self.HL) - 1][i] * self.Links[i + FirstLink][
                    j])  # и плюсуем к результату, нейрон умноженный на вес
                # print(Links[i+FirstLink][j])
            self.outValues[j] = res
    # -------------------------------------- End of netCalc -----------------------------------------------------------

    # ======================================  процедура отображения нейронной сети ====================================
    # пока без параметров, просто отображаем массивы
    # =================================================================================================================
    def showNet(self):
        print('In Values: ', self.inValues)
        # print('Hiden layers:', HL)
        for i in range(len(self.Links)):
            print('Links layer ', str(i), ' :', self.Links[i])
        for i in range(len(self.HL)):
            print('Hidden Layer ', str(i), ' :', self.HL[i])
        print('Out Values:', self.outValues)
    # -------------------------------------- End of showNet -----------------------------------------------------------

    # ======================================  процедура создания нейронной сети =======================================
    # inValuesP - кол-во входящих параметров; #NeronLayerP - кол-во нейронов в [каждом скрытом слое];
    # #outValuesP - количество выходных параметров
    # задается сл. образом: iCreate(3,2,[3,5],2) - 3 входящих параметра, 2 скрытых слоя, размер первого 3, второго 5,
    # 2 вых. параметра
    # =================================================================================================================
    def iCreate(self, inValuesP, NeronLayerP, outValuesP):

        # инициализируем датасеты
        # self.initDataset()

        # подготавливаем массивы
        self.prepareArrays(inValuesP, NeronLayerP, outValuesP, -1, 1, 2)
    # -------------------------------------- End of iCreate -----------------------------------------------------------

    # ======================================  процедура корректировки весов Link у наследников ========================
    # веса корректируются на всех линках в пределах от -1 до +1
    # divVal - коэфициент деления для рандома, т.е.
    # если divVal = 10 то корректировка -0.1 до +0.1 если divVal = 100 то -0.01 до +0.01 и тд
    # =================================================================================================================
    def InhReLink(self, divVal):
        # print('всего линков: ' , str(len(self.Links)))
        for i in range(len(self.Links)):
            # print(' линк ', str(i),' ',str(len(self.Links[i])))
            for j in range(len(self.Links[i])):
                k = self.initVal(-1, 1, 10)
                self.Links[i][j] = self.Links[i][j] + k / divVal

    # -------------------------------------- End of InhReLink ---------------------------------------------------------

    # ======================================  функция рассчета ошибки =================================================
    # функция вычитает expect - outValue, возвращает разницу
    # =================================================================================================================
    def calcError(self, expect):
        res = abs(expect - self.outValues[0])
        return res
    # -------------------------------------- End of calcError ---------------------------------------------------------

    # ****************************************************************************************************************#
    #                   Инициализация, описания процедур для обучения сети в рамках класс NN                          #
    # ****************************************************************************************************************#

    # ======================================  функция обработки данных одним поколением ===============================
    # InhCount - количество потомков
    # =================================================================================================================
    def oneGeneration(self, Net, InhCount):
        # создаем потомков нейронной сети (Inheriteds)
        Inh = []
        for i in range(0, InhCount):        # создаем InhCount потомков
            Inh.append(NN())                # создаем нового потомка
            Inh[i] = copy.deepcopy(Net)     # копируем потомку нашу сеть
            Inh[i].InhReLink(100)           # модифицируем для него линки
            Inh[i].netCalc()                # проводим расчет сети потомка
    # -------------------------------------- End of oneGeneration -----------------------------------------------------

    # ======================================  функция обучения сети ===================================================
    # show = 0 - ничего не показывать  1 - показывать showNet() 2 показывать showNet() + комменты
    # 9 - просмотр, без обучения
    # =================================================================================================================
    def learnNet(self, net, show):
        #global net

        if show in (2, 3, 9):
            print('\n Начинаем обучение сети \nКоличество входящих значений: ', str(len(net.inValues)))
            print('Количество обучающих дата-сетов: ', str(len(self.valInValues)))  # + valExpect

        for i in range(len(self.valInValues)):  # перебираем весь обучающий дата-сет, проводя одну эпоху обучения
            net.inValues = self.valInValues[i][0]   # устанавливаем i-й датасет для обучения
            net.netCalc()                           # расчитываем сеть
            Err = net.calcError(self.valInValues[i][1])  # высчитываем ошибку для i-го ожидаемого результата

            if show in (2, 3, 9):
                if self.valInValues[i][1] != 0:  # вычисляем точность в %
                    ErrPrc = round(net.outValues[0] * 100 / self.valInValues[i][1], 2)
                else:
                    ErrPrc = 0
                print(self.valInValues[i][0], ' Выборка ', str(i + 1), ' из ', str(len(self.valInValues)), ' Ответ:',
                      str(net.outValues[0]), ' ожидаем:', str(self.valInValues[i][1]), ' Error = ', str(round(Err, 2)), ' (',
                      str(ErrPrc), '%)')

            if show in (1, 3):
                net.showNet()

            if show != 9:  # 9 - просмотровый режим, в нем сеть не обучаем
                # создаем потомков нейронной сети (Inheriteds)
                Inh = []
                BestInh = -1
                for j in range(0, 7):               # создаем InhCount потомков
                    Inh.append(NN())                # создаем нового потомка
                    Inh[j] = copy.deepcopy(net)     # копируем потомку нашу сеть
                    Inh[j].InhReLink(100)           # модифицируем для него линки +/- 1/100
                    Inh[j].netCalc()                # проводим расчет сети потомка
                    InhErr = Inh[j].calcError(self.valInValues[i][1])  # расчет ошибки

                    if InhErr < Err:
                        BestInh = j  # устанавливаем "Лучшим" № наследника если у него ошибка меньше чем у исходной сети или предыдущего
                        Err = InhErr

                    if show == 3:
                        print(InhErr)

                if BestInh > -1:  # если есть лучший потомок чем исходная сеть
                    net = copy.deepcopy(Inh[BestInh])  # замещаем им нашу сеть

            if show == 3:
                print('Best = ', str(BestInh))
                print(' --- ')

        return net
    # -------------------------------------- End of learnNet ----------------------------------------------------------

    # =======================================  функция дополнения данными =============================================
    # обучающего = 0 или тестового = 1 датасета
    # =================================================================================================================
    def addToDataset(self, dataSet, arr):
        # учим сеть конвертации двоичная в десятичная
        # #заполняем обущающий дата-сет
        if dataSet == 0:
            self.learnDataSet.append(arr)

        if dataSet == 1:
            self.testDataSet.append(arr)

    # -------------------------------------- End of SetDataset --------------------------------------------------------

    # ======================================  функция заполнения данными обучающей и тестовой =========================
    # learnDataSet = [] #обучающая выборка состоит из набора разных inValues[]
    # testDataSet = []  #контрольная выборка состоит из набора разных inValues[]
    # =================================================================================================================
    def initDataset(self):
        # учим сеть конвертации двоичная в десятичная
        # #заполняем обущающий дата-сет
        self.addToDataset(0, [[0, 0, 0, 1], 1])
        self.addToDataset(0, [[0, 1, 0, 0], 4])
        self.addToDataset(0, [[1, 0, 0, 0], 8])
        self.addToDataset(0, [[1, 0, 0, 1], 9])
        self.addToDataset(0, [[0, 1, 1, 0], 6])

        # #заполняем тестовый дата-сет
        self.addToDataset(1, [[0, 1, 1, 1], 7])
        self.addToDataset(1, [[1, 1, 0, 0], 12])
        self.addToDataset(1, [[1, 0, 1, 0], 10])
        self.addToDataset(1, [[1, 1, 1, 0], 14])
        self.addToDataset(1, [[1, 1, 1, 1], 15])
    # -------------------------------------- End of SetDataset --------------------------------------------------------

    # ======================================  функция формирования обучающего датасета ================================
    # inData: 0 - обучающая выборка; 1 - контрольная выборка
    # =================================================================================================================
    def setDataset(self, inData):
        self.valInValues = []
        self.valExpect = []

        if inData == 0:
            self.valInValues = self.learnDataSet
         #   self.valExpect = self.learnExpect

        if inData == 1:
            self.valInValues = self.testDataSet
         #   self.valExpect = self.testExpect
    # -------------------------------------- End of SetDataset --------------------------------------------------------


