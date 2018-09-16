import testing
import time
import random
time00 = time.time()
temp = 0
while temp < 60000:
	temp += 1
	point1 = (random.uniform(50,150),random.uniform(70,100))
	point2 = (random.uniform(50,150),random.uniform(70,100))
time0 = time.time()
print(time0-time00)
time1 = time.time()
temp = 0
while temp < 60000:
	temp += 1
	# point1 = (random.uniform(50,150),random.uniform(70,100))
	# point2 = (random.uniform(50,150),random.uniform(70,100))
	point1 = (50,50)
	point2 = (153,80.5)
	testing.get_final_distance(point1,point2)
	# if temp % 600 == 0:
time2 = time.time()
print(time2-time1)





# import numpy as np
# a = np.array([1,-1])
# b = np.array([-1,0])
# la = np.sqrt(a.dot(a))
# lb = np.sqrt(b.dot(b))
# angle = np.arccos(a.dot(b)/(la*lb))
# print(angle*360/2/np.pi)
# print(time4-time3) #0.0768
# print(time2-time1) #153.536