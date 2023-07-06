#from keras.models import Sequential
#from keras.layers import Dense
import numpy as np

X = np.random.randn(4, 3)
Y = np.array([[1,2,3],
              [2,3,4],
              [3,4,5],
              [4,5,6]])
#print(X)
#print(Y)


mylist = {1: 1,
          2: 'какая-то вторая строка',
          3: 3}

mylist[4] = 'добавили динамически'

print(mylist)
#print(mylist.get(2))

transform = {'Sex': lambda gen: {'male': 0, 'female': 1}.get(gen)}

arr = ['male', 'female', 'female', 'male', 'male']

print(arr)
print('')

for i in arr:
    #arr_f =
    print(i)

#lam = lambda x: x * 4
#print (lam(Y))