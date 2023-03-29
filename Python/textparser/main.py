import csv

# открываем файл в режиме чтения
f = open('list.txt', 'r')

# открываем файл в режиме записи
fw = open('tmp.txt', 'w')

wList = []

with open('testcsv.csv', encoding='UTF-8') as r_file:
    fr = csv.reader(r_file, delimiter=";")

    for row in fr:
        # print(row[0])

        # читаем в t содержимое
        t = row[0]  # f.read()

        alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
                    "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

        # print(t)
        print(len(t))

        # преобразуем в нижний регистр
        t = t.lower()

        nT = ''

        # проверяем каждый символ строки
        for iS in t:
            if iS in alphabet:  # если символ в нашем алфавите то плюсуем к строке чтобы получить слово
                nT += iS
            else:  # если символа в строке нету то обнуляем переменную и если слово больше 0 то добавляем в список
                if len(nT) > 1:  # если длина слова больше 0 начинаем обработку
                    off = 0  # обнуляем признак "наличия записи"
                    for i in range(len(wList)):  # начинаем поиск
                        if wList[i][1] == nT:  # если нашли совпадение слова
                            wList[i][0] += 1  # плюсуем к количеству
                            off = 1  # и обнуляем признак наличия

                    if off == 0:  # если признак наличия = 0 то добавляем слово
                        aT = [1, nT]
                        wList.append(aT)

                    nT = ''

        wList.sort()

print(len(wList))
print(wList)

for i in range(len(wList)):
    print(wList[i][1], '-', wList[i][0])

# закрываем файл
f.close()