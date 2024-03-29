from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt

# Генерация данных для обучения
#X = np.random.randn(100, 3)
#y = np.random.randn(100, 1)
# X - массив для обучения, 3 нейрона на входе, имеем 5 массивов, 5 наборов данных
X = np.array([[0, 0, 1],
              [0, 1, 0],
          #    [0, 1, 1],
              [1, 0, 0],
              [1, 0, 1],
          #    [1, 1, 0],
              [1, 1, 1]
              ])

# Y - массив ожидаемых результатов для обучения, на выходе 2 нейрона, по этому 5 массивов (для каждого Х) по 2 ответа в каждом
y = np.array([[1, 1],
              [2, 1],
              [4, 1],
              [5, 2],
              [7, 3]])

# Создание модели нейронной сети
# так как учим сеть конвертировать в десятичную из двоичной и считать функции активации оставляем линейными
model = Sequential()
model.add(Dense(4, input_dim=3))   # это значит 3 входящих нейрона, 4 нейрона на выходе
model.add(Dense(2))                # еще один слой - вход идет с прошлого слоя, на выходе 2 нейрона

print('Compile model...')
# Компиляция модели
model.compile(loss='mean_squared_error', optimizer='sgd')

print('Starting fit...')
# Обучение модели verbose=0 - не отображать инфо об обучении, эпохах
history = model.fit(X, y, epochs=500, verbose=0)

# Оценка качества модели на новых данных
# X_test = np.random.randn(10, 3)
# y_test = np.random.randn(10, 1)

X_test = np.array([[0, 1, 1],
                   [1, 1, 0]])
y_test = np.array([[3, 2],
                   [6, 2]])

loss = model.evaluate(X_test, y_test)
print('Test Loss:', loss)

predicted = model.predict(X_test)
print(predicted)

# Обучение и проверка величины потерь
plt.plot(history.history['loss'])
#plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()