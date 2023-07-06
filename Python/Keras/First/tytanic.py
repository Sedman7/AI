#import keras as k
import numpy as np
import pandas as pd

# читаем данные из csv в data_frame из файла
# data_frame - основной класс pandas для чтения таблиц
data_frame = pd.read_csv('titanic.csv')

#[=============   информация по Pandas =======================]
#print(data_frame) # выводим весь список
#print(data_frame.head(n=5)) # выводим 5 первых строк списка
#print(data_frame['Age']) # вывести одну колонку

#input_names = ['Age', 'Name']   # создаем переменную для вывода нескольких колонок
#print(data_frame[input_names])  # передаем переменную в data_frame, можно нарушая порядок колонок

#print(data_frame['Age'].max()) # вывести максимальное значение колонки Age
#print(data_frame['Sex'].unique()) # вывести уникальные значения колонки Sex

# формируем 2 переменные input_names - входные данные output_names - выходные данные
input_names = ['Age', 'Sex', 'Pclass']
output_names = ['Survived']

#print(data_frame[output_names])

# подготавливаем данные, копируем в "сырые" переменные нужные нам колонки
# приступаем к нормализации данных
max_age = 100  #максимальный возраст пассажира
encoders = {'Age': lambda age: age/max_age,
            'Sex': lambda gen: {'male': 0, 'female': 1}.get(gen),
            'Pclass': lambda pclass: {1: [1, 0, 0], 2: [0, 1, 0], 3: [0, 0, 1]}.get(pclass)}

def dataframe_to_dict(df):
    print(df.columns)
    result = dict()
    for column in df.columns:
        values = data_frame[column].values
        result[column] = values
    print(result)
    return result

def make_supervised(df):
    raw_input_data = data_frame[input_names]
    raw_output_data = data_frame[output_names]
    return {'inputs': dataframe_to_dict(raw_input_data),
            'outputs': dataframe_to_dict(raw_output_data)}

supervised = make_supervised(data_frame)
#print(supervised)