import numpy as np
import queue
from PIL import Image
from neuron import init_network, get_neighborhood
from testing import initialize, get_final_distance
from image_process import read_image
import data_generator
import multiprocessing
import time

global im,mlength,mheight

def select_closest(network, city,unused):
	# min = float('inf')
	d_list = []
	while(len(d_list) != 0):
		d_list.pop()
	min_index = -1
	pool = multiprocessing.Pool(processes=50)
	for i in range(len(network)):
		# print(get_unwall(network[i][0],network[i][1]))
		# print((city[0],city[1]))
		# d_list.append(get_final_distance(get_unwall(network[i][0],network[i][1]),(city[0],city[1])))
		d_list.append((pool.apply_async(get_dis_in_pool, args=(network, city, i, )), i))
	pool.close()
	pool.join()
#	print(len(d_list))
	# if d < min and unused[i]:
	# 	min = d
	# 	min_index = i
#	print(d_list)
	p_list = []
	q_list = []
	for res in d_list:
		p_list.append((res[0].get(),res[1]))
	for i in range(len(p_list)):
		q_list.append(p_list[i][0])
	min_index = p_list.index(min(p_list))
	min_index = d_list[min_index][1]
	##
	##
	###此处改多进程
	unused[min_index] = False 
	return min_index

def get_dis_in_pool(network,city,i):
	return (get_final_distance(get_unwall(network[i][0],network[i][1]),(city[0],city[1])), i)

def get_unwall(x,y):
	if im[int(x)][int(y)] == 1:
		return (x,y)
	else:
		q = queue.Queue()
		q.put((int(x),int(y)))
		visited = [[False] * mlength] * mheight
		visited[int(x)][int(y)] = True
		while not q.empty():
			(tmpx,tmpy) = q.get()
			for i in range(tmpx - 1,tmpx + 2):
				for k in range(tmpy - 1,tmpy + 2):
					if i >= 0 and i < mlength and k >= 0 and k < mheight:
						if im[i][k] == 1:
							return(i,k)
						elif visited[i][k] == False:
							visited[i][k] = True
							q.put((i,k))

def som(cities, epoches, learning_rate = 0.8):
	num_neuron = len(cities) * 12
	network = np.array(init_network(num_neuron,im,mlength,mheight))
	n = num_neuron
	for i in range(epoches):
		np.random.shuffle(cities)
		unused = [True] * num_neuron
		for k in range(len(cities)):
			winner_idx = select_closest(network, cities[k],unused)
			gaussian = get_neighborhood(winner_idx, n//10, num_neuron)
			network += gaussian[:,np.newaxis] * learning_rate * (cities[k] - network)
			learning_rate *= 0.9997
			n = n * 0.997
		'''
		unused = [True] * num_neuron
		tmplist = []
		for city in cities:
			tmplist.append(select_closest(network,city,unused))
		sorted(tmplist)

		print_list = []
		for kl in tmplist:
			print_list.append(network[kl])
'''
		print('epoch {epoch_num}, learning_rate {lr}, num_neuron {nu}'.format(epoch_num=i,lr=learning_rate,nu=n))
	#	print(print_list)
		if n < 1 or learning_rate < 0.001:
			break
	
	unused = [True] * num_neuron
	for i in range(len(cities)):
		cities[i].append(select_closest(network, cities[i], unused))
	cities = sorted(cities,key = lambda x:x[2])
	return cities

if __name__ == '__main__':
	print(time.asctime(time.localtime(time.time())))
	ratio = 2
	(im,mlength,mheight) = read_image('./a.pgm',ratio)
	cities = data_generator.data_generate(100,im,mlength,mheight)
	initialize(im,mlength,mheight)
	# cities = [[111, 151, 7], [112, 154, 17], [114, 149, 26], [118, 150, 37], [134, 150, 46], [137, 157, 57], [144, 156, 66], [141, 161, 75], [139, 167, 85], [132, 161, 94], [132, 159, 103], [130, 157, 113], [116, 158, 124], [105, 158, 133], [105, 164, 143], [98, 161, 153], [93, 158, 163], [86, 155, 172], [85, 164, 183], [77, 164, 193], [69, 170, 203], [68, 160, 213], [62, 163, 223], [61, 153, 233], [52, 149, 242], [45, 148, 252], [54, 145, 262], [62, 133, 271], [54, 120, 285], [67, 118, 296], [65, 111, 306], [54, 111, 316], [58, 108, 327], [61, 97, 336], [55, 92, 345], [63, 90, 354], [60, 87, 363], [64, 85, 372], [60, 79, 381], [50, 83, 392], [47, 83, 401], [48, 71, 412], [53, 70, 422], [52, 60, 433], [44, 45, 445], [39, 42, 457], [38, 34, 469], [46, 33, 482], [50, 40, 495], [53, 42, 507], [51, 47, 519], [53, 47, 531], [58, 43, 544], [65, 43, 557], [69, 50, 570], [70, 51, 582], [77, 32, 597], [103, 23, 612], [106, 23, 621], [112, 24, 630], [118, 27, 638], [125, 21, 646], [123, 36, 654], [122, 34, 661], [119, 31, 669], [109, 29, 677], [108, 30, 684], [108, 31, 691], [108, 31, 692], [103, 29, 700], [103, 33, 707], [102, 42, 715], [98, 44, 721], [91, 44, 724], [76, 46, 725], [86, 51, 803], [88, 56, 804], [91, 70, 806], [85, 72, 808], [81, 71, 810], [78, 67, 812], [81, 64, 815], [79, 62, 818], [61, 68, 825], [67, 71, 834], [71, 73, 843], [71, 93, 854], [82, 93, 864], [88, 98, 874], [94, 107, 884], [95, 109, 894], [78, 106, 906], [76, 114, 916], [80, 118, 927], [86, 116, 938], [87, 132, 950], [82, 139, 961], [77, 138, 972], [81, 149, 984], [89, 144, 995]]
	# print_image(cities,ratio)
	time2 = time.time()
	print(som(cities,1500))
	# print(time.asctime(time.localtime(time.time())))

