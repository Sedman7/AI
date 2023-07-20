import keras as k
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
encoders = {'Age': lambda age: [age/max_age],
            'Sex': lambda gen: {'male': [0], 'female': [1]}.get(gen),
            'Pclass': lambda pclass: {1: [1, 0, 0], 2: [0, 1, 0], 3: [0, 0, 1]}.get(pclass),
            "Survived": lambda s_value: [s_value]}

#тут преобразуем данные в словарь
def dataframe_to_dict(df):
    print(df.columns)
    result = dict()
    for column in df.columns:
        values = data_frame[column].values
        result[column] = values
    #print(result)
    return result

def make_supervised(df):
    raw_input_data = data_frame[input_names]
    raw_output_data = data_frame[output_names]
    return {'inputs': dataframe_to_dict(raw_input_data),
            'outputs': dataframe_to_dict(raw_output_data)}

def encode(data):
    vectors = []
    for data_name, data_values in data.items():
        encoded = list(map(encoders[data_name], data_values))
        vectors.append(encoded)
    #print(vectors)
    formatted = []
    for vector_raw in list(zip(*vectors)):
        vector = []
        for element in vector_raw:
            for e in element:
                vector.append(e)
        formatted.append(vector)
    return formatted

supervised = make_supervised(data_frame)
encoded_inputs = np.array(encode(supervised["inputs"]))
encoded_outputs = np.array(encode(supervised["outputs"]))

#разделим данные на тренировочные и проверочные
train_x = encoded_inputs[:600]     #помним что 600-й элемент не включается т.е. 0-599
train_y = encoded_outputs[:600]

test_x = encoded_inputs[600:]
test_y = encoded_outputs[600:]

model = k.Sequential()
model.add(k.layers.Dense(3, input_dim=5))   # это значит 3 входящих нейрона, 4 нейрона на выходе
#model.add(k.layers.Dense(units=5, activation="relu"))
model.add(k.layers.Dense(units=1, activation="sigmoid"))

model.compile(loss="mse", optimizer="sgd", metrics=["accuracy"])  #для многоклассовой классификации пишем acc

#тренеруем модель или
fit_results = model.fit(x=train_x, y=train_y, epochs=300, validation_split=0.2, verbose=2) #validation_split=0.2 - значит что 80% пойдет на тренеровку и 20% на валидацию
#или загружаем модель из файла (если сохраняли раньше)
#model.load_weights("weights.h5")

#если модель получилась удачной - сохраняем наши веса
#model.save_weights("weights.h5")

# #визуализируем нашу модель
plt.title("Loo and train validation")
plt.plot(fit_results.history["loss"], label="Train")
plt.plot(fit_results.history["val_loss"], label="Validation")
plt.legend
plt.show()
#
# plt.title("accuracy and train validation")
# plt.plot(fit_results.history["accuracy"], label="Train")
# plt.plot(fit_results.history["val_accuracy"], label="Validation")
# plt.legend
# plt.show()

test_x2 = [[0.20, 1, 1, 0, 0], [0.30, 1, 1, 0, 0], [0.40, 1, 1, 0, 0],
           [0.20, 0, 1, 0, 0], [0.30, 0, 1, 0, 0], [0.40, 0, 1, 0, 0]]

predicted_test = model.predict(test_x2)
print(predicted_test)
#real_data = data_frame.iloc[600:][input_names+output_names]
#real_data["PSurvived"] = predicted_test
#print(real_data)