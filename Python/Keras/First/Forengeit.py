import keras as k
import numpy as np
import matplotlib.pyplot as plt

c = np.array([-40, -30, -20, -10, 0, 5, 8, 15, 22, 38, 40, 45, 55, 1, 19, -37, 200, -100, 140, -15, 12.2])
f = np.array([-40, -22, -4, 14, 32, 36, 41, 59, 72, 100, 104, 113, 131, 33.8, 66.2, -34.6, 392, -148, 284, 5, 53.96])

model = k.Sequential()
model.add(k.layers.Dense(units=1, input_shape=(1,), activation='linear')) #units=1 - сколько нейронов в слое; input_shape=(1,) - сколько входов

#model.compile(loss="mse", optimizer=k.optimizers.Adam(0.25))
model.compile(loss="mse", optimizer="RMSprop")


history = model.fit(c, f, epochs=500, validation_split=0.2)

# #визуализируем нашу модель
plt.title("Loo and train validation")
plt.plot(history.history["loss"], label="Train")
plt.plot(history.history["val_loss"], label="Validation")
plt.legend
plt.show()

test = np.array([-25, 10, 50 ,100])

predicted = model.predict(test)
print(predicted)
