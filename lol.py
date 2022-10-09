import numpy as np
import time


start = time.time()
for i in range(100000):
	result = "".join(list(map(str, np.array([[np.random.random(),np.random.random(),np.random.random()],[np.random.random(), np.random.random(), np.random.random()]]).flatten())))
end = time.time()
print(end - start)

start = time.time()
for i in range(1):
	arr = [[np.random.random(),np.random.random(),np.random.random()],[np.random.random(), np.random.random(), np.random.random()]]
	mystr = ''
	for a in range(2):
		for b in range(3):
			mystr += str(arr[a][b])
# end = time.time()
# print(end - start)