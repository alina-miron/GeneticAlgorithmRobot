import random
import matplotlib.pyplot as plt;
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(0, 10000000):
    randomNumber = random.randint(0, 9)
    array[randomNumber] += 1

print(array)

# Instructions to display the array
objects = ('1', '2', '3', '4', '5',
           '6','7','8','9','10')
y_pos = np.arange(len(objects))

plt.bar(y_pos, array, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Number generated')
plt.title('Random number generator')

plt.show()