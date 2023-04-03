# подключаем модуль для лематизации
import pymorphy2


morph = pymorphy2.MorphAnalyzer()

# исходный текст
text = "Съешь еще этих мягких французских булок да выпей чаю"

# определяем процедуру лематизации
def lemmatize(text):
    words = text.split() # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)

    return res

print(lemmatize(text))