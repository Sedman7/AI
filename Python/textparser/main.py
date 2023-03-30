import csv


f = open('list.txt', 'r')   # открываем файл в режиме чтения

fw = open('tmp.txt', 'w')   # открываем файл в режиме записи

wList = []  # words list - список найденных слов

alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
            "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

def WordCheck(cWord):
    off = 0                         # по умолчанию результат = 0
    for i in range(len(wList)):     # начинаем поиск
        if wList[i][1] == cWord:    # если нашли совпадение слова
            wList[i][0] += 1        # плюсуем к количеству
            off = 1                 # слово было найдено среди имеющихся, значит = 1

    if off == 0:                    # если признак наличия = 0 то добавляем слово
        aT = [1, cWord]
        wList.append(aT)

    return off

#работа с csv файлами
with open('testcsv.csv', encoding='UTF-8') as r_file:   # открываем файл
    fr = csv.reader(r_file, delimiter=";")              # читаем файл в переменную, установив разделитель в ;

    for row in fr:                  # проходим по всем рядам в файле
        # print(row[0])

        t = row[0]  # f.read()      # читаем в t содержимое

        #print(t)
        print(len(t))

        t = t.lower()               # преобразуем в нижний регистр

        nT = ''

        # проверяем каждый символ строки
        for iS in t:
            if iS in alphabet:  # если символ в нашем алфавите то плюсуем к строке чтобы получить слово
                nT += iS
            else:               # если символа в строке нету
                if len(nT) > 1:     # если длина слова больше 0 начинаем обработку
                    WordCheck(nT)   # проверяем есть ли слово в уже найденых
                    nT = ''         # обнуляем "временное" слово

        if len(nT) > 1:     # если длина слова больше 0 начинаем обработку
            WordCheck(nT)   # проверяем есть ли слово в уже найденых
            nT = ''

        wList.sort()

print(len(wList))
print(wList)

*res, = filter(lambda x: x[1] == 1, wList)
print(res)

#for i in range(len(wList)):
#    print(wList[i][1], '-', wList[i][0])

# закрываем файл
f.close()