import numpy as np
import queue
from PIL import Image
from neuron import init_network, get_neighborhood
from testing import initialize, get_final_distance
from image_process import read_image
import data_generator

global im,mlength,mheight

def select_closest(network, city,unused):
	min = float('inf')
	min_index = -1
	for i in range(len(network)):
		# print(get_unwall(network[i][0],network[i][1]))
		# print((city[0],city[1]))
		d = get_final_distance(get_unwall(network[i][0],network[i][1]),(city[0],city[1])) 
		if d < min and unused[i]:
			min = d
			min_index = i
	unused[min_index] = False 
	return min_index

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
	num_neuron = len(cities) * 8
	network = np.array(init_network(num_neuron,im,mlength,mheight))
	n = num_neuron
	for i in range(epoches):
		np.random.shuffle(cities)
		unused = [True] * num_neuron
		for k in range(len(cities)):
			winner_idx = select_closest(network, cities[k],unused)
			gaussian = get_neighborhood(winner_idx, n//10, num_neuron)
			network += gaussian[:,np.newaxis] * learning_rate * (cities[k] - network)
			learning_rate *= 0.99997
			n = n * 0.9997
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
	(im,mlength,mheight) = read_image('./a.pgm',2)
	cities = data_generator.data_generate(10,im,mlength,mheight)


	initialize(im,mlength,mheight)
	print(som(cities,1500))
