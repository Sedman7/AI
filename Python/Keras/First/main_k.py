import keras as k
import numpy as np

#создаем x-входящие значения и y-одижаемые и сразу их оборачиваем в массив numpy
input_data = np.array([0.3, 0.7, 0.9])
output_data = np.array([0.5, 0.9, 1.0])

model = k.Sequential()
#model.add(k.layers.Dense(units=1, input_shape=(1,), activation='linear'))
model.add(k.layers.Dense(units=1, input_shape=(1,), activation='sigmoid'))
model.compile(loss="mse", optimizer="sgd")

fit_results = model.fit(x=input_data, y=output_data, epochs=100)

predicted = model.predict([0.5])
print(predicted)

X = np.random.randn(10, 3)
print(X)