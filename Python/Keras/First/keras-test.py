from keras.models import Sequential
from keras.layers import Dense
import numpy as np

X = np.random.randn(4, 3)
Y = np.array([[1,2,3],
              [2,3,4],
              [3,4,5],
              [4,5,6]])
print(X)
print(Y)
