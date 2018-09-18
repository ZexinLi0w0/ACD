import math
import copy
import cv2
import queue
import time
import os
from PIL import Image
import numpy as np

graph = []
	
def pretreatment(old_graph):
	np_graph = np.array(old_graph)
	store = []
	temp = []
	delete = []
	q = queue.Queue()

	for i in range(np_graph.shape[0]):
		for j in range(np_graph.shape[1]):
			if np_graph[i][j] == 1:
				store.append((i,j))
	all_point_num = len(store)
	while not len(store) == 0:
		q.put(store.pop())
		while not q.empty():
			temp_point = q.get()
			temp.append(temp_point)
			if np_graph[temp_point[0] - 1][temp_point[1]] == 1 and (temp_point[0] - 1,temp_point[1]) in store:
				store.remove((temp_point[0] - 1,temp_point[1]))
				q.put((temp_point[0] - 1,temp_point[1]))
			if np_graph[temp_point[0] + 1][temp_point[1]] == 1 and (temp_point[0] + 1,temp_point[1]) in store:
				store.remove((temp_point[0] + 1,temp_point[1]))
				q.put((temp_point[0] + 1,temp_point[1]))
			if np_graph[temp_point[0]][temp_point[1] - 1] == 1 and (temp_point[0],temp_point[1] - 1) in store:
				store.remove((temp_point[0],temp_point[1] - 1))
				q.put((temp_point[0],temp_point[1] - 1))
			if np_graph[temp_point[0]][temp_point[1] + 1] == 1 and (temp_point[0],temp_point[1] + 1) in store:
				store.remove((temp_point[0],temp_point[1] + 1))
				q.put((temp_point[0],temp_point[1] + 1))
			if np_graph[temp_point[0] - 1][temp_point[1] - 1] == 1 and (temp_point[0] - 1,temp_point[1] - 1) in store:
				store.remove((temp_point[0] - 1,temp_point[1] - 1))
				q.put((temp_point[0] - 1,temp_point[1] - 1))
			if np_graph[temp_point[0] + 1][temp_point[1] + 1] == 1 and (temp_point[0] + 1,temp_point[1] + 1) in store:
				store.remove((temp_point[0] + 1,temp_point[1] + 1))
				q.put((temp_point[0] + 1,temp_point[1]))
			if np_graph[temp_point[0] + 1][temp_point[1] - 1] == 1 and (temp_point[0] + 1,temp_point[1] - 1) in store:
				store.remove((temp_point[0] + 1,temp_point[1] - 1))
				q.put((temp_point[0] + 1,temp_point[1] - 1))
			if np_graph[temp_point[0] - 1][temp_point[1] + 1] == 1 and (temp_point[0] - 1,temp_point[1] + 1) in store:
				store.remove((temp_point[0] - 1,temp_point[1] + 1))
				q.put((temp_point[0] - 1,temp_point[1] + 1))
		if len(temp) > 0.9 * all_point_num:
			break
		while not len(temp) == 0:
			delete.append(temp.pop())
	for point in store:
		np_graph[point[0]][point[1]] = 0
	for point in delete:
		np_graph[point[0]][point[1]] = 0
	#return ordered graph
	return np_graph

def count(x,y):
	point_num = 0
	if graph[x - 1][y - 1] == 1:
		point_num += 1
	if graph[x - 1][y] == 1:
		point_num += 1
	if graph[x - 1][y + 1] == 1:
		point_num += 1
	if graph[x][y - 1] == 1:
		point_num += 1

	if graph[x][y + 1] == 1:
		point_num += 1
	if graph[x + 1][y - 1] == 1:
		point_num += 1
	if graph[x + 1][y] == 1:
		point_num += 1
	if graph[x + 1][y + 1] == 1:
		point_num += 1
	return point_num

def find_x_range(list):
	minx_point = (248,248)
	maxx_point = (0,0)
	for point in list:
		if point[0] < minx_point[0]:
			minx_point = (point[0],point[1])
		if point[0] > maxx_point[0]:
			maxx_point = (point[0],point[1])
	
	return (minx_point,maxx_point)

def find_border(graph,row,column):
	list = []
	for i in range(row):
		for j in range(column):
			if graph[i][j] == 1:
				# temp = count(i,j)
				point_num = 0
				if graph[i - 1][j - 1] == 1:
					point_num += 1
				if graph[i - 1][j] == 1:
					point_num += 1
				if graph[i - 1][j + 1] == 1:
					point_num += 1
				if graph[i][j - 1] == 1:
					point_num += 1

				if graph[i][j + 1] == 1:
					point_num += 1
				if graph[i + 1][j - 1] == 1:
					point_num += 1
				if graph[i + 1][j] == 1:
					point_num += 1
				if graph[i + 1][j + 1] == 1:
					point_num += 1
				if point_num < 8 and point_num > 0:
					list.append((i,j))

	out_border = []
	in_border = []
	temp_queue = queue.Queue()
	store = []
	max_num = 0
	while not len(list) == 0:
		li = []
		temp_queue.put(list.pop())
		while not temp_queue.empty():
			temp = temp_queue.get()
			store.append(temp)
			if graph[temp[0] - 1][temp[1]] == 1 and (temp[0] - 1,temp[1]) in list:
				list.remove((temp[0] - 1,temp[1]))
				temp_queue.put((temp[0] - 1,temp[1]))
			if graph[temp[0] + 1][temp[1]] == 1 and (temp[0] + 1,temp[1]) in list:
				list.remove((temp[0] + 1,temp[1]))
				temp_queue.put((temp[0] + 1,temp[1]))
			if graph[temp[0]][temp[1] - 1] == 1 and (temp[0],temp[1] - 1) in list:
				list.remove((temp[0],temp[1] - 1))
				temp_queue.put((temp[0],temp[1] - 1))
			if graph[temp[0]][temp[1] + 1] == 1 and (temp[0],temp[1] + 1) in list:
				list.remove((temp[0],temp[1] + 1))
				temp_queue.put((temp[0],temp[1] + 1))
			if graph[temp[0] - 1][temp[1] + 1] == 1 and (temp[0] - 1,temp[1] + 1) in list:
				list.remove((temp[0] - 1,temp[1] + 1))
				temp_queue.put((temp[0] - 1,temp[1] + 1))
			if graph[temp[0] + 1][temp[1] + 1] == 1 and (temp[0] + 1,temp[1] + 1) in list:
				list.remove((temp[0] + 1,temp[1] + 1))
				temp_queue.put((temp[0] + 1,temp[1] + 1))
			if graph[temp[0] - 1][temp[1] - 1] == 1 and (temp[0] - 1,temp[1] - 1) in list:
				list.remove((temp[0] - 1,temp[1] - 1))
				temp_queue.put((temp[0] - 1,temp[1] - 1))
			if graph[temp[0] + 1][temp[1] - 1] == 1 and (temp[0] + 1,temp[1] - 1) in list:
				list.remove((temp[0] + 1,temp[1] - 1))
				temp_queue.put((temp[0] + 1,temp[1] - 1))
		while not len(store) == 0:
			li.append(store.pop())
		max_num = max_num if max_num > len(li) else len(li)
		in_border.append(li)

	for points in in_border:
		if len(points) == max_num:
			out_border.append(points)
			in_border.remove(points)

	return (out_border,in_border)
# 此处要修改成返回有序点链---chain
# 内边界要求顺时针序，外边界要求逆时针序（可直接返回一个顺时针序，写入时给外边界反序）
	
def sort_incw(old_out,old_inp):
	out = copy.deepcopy(old_out)
	inp = copy.deepcopy(old_inp)
	inpc = []
	for points in out:
		stack = []
		visited = [[0 for row in range(248)] for col in range(248)]
		size = len(points)
		(maxp,minp) = find_x_range(points)
		stack.append(minp)
		visited[minp[0]][minp[1]] = 1
		while True:
			# 左上右下
			if visited[stack[-1][0]][stack[-1][1] - 1] == 0 and (stack[-1][0],stack[-1][1] - 1) in points:
				visited[stack[-1][0]][stack[-1][1] - 1] = 1
				stack.append((stack[-1][0],stack[-1][1] - 1))
				continue
			if visited[stack[-1][0] - 1][stack[-1][1] - 1] == 0 and (stack[-1][0] - 1,stack[-1][1] - 1) in points:
				visited[stack[-1][0] - 1][stack[-1][1] - 1] = 1
				stack.append((stack[-1][0] - 1,stack[-1][1] - 1))
				continue
			if visited[stack[-1][0] - 1][stack[-1][1]] == 0 and (stack[-1][0] - 1,stack[-1][1]) in points:
				visited[stack[-1][0] - 1][stack[-1][1]] = 1
				stack.append((stack[-1][0] - 1,stack[-1][1]))
				continue
			if visited[stack[-1][0] - 1][stack[-1][1] + 1] == 0 and (stack[-1][0] - 1,stack[-1][1] + 1) in points:
				visited[stack[-1][0] - 1][stack[-1][1] + 1] = 1
				stack.append((stack[-1][0] - 1,stack[-1][1] + 1))
				continue
			if visited[stack[-1][0]][stack[-1][1] + 1] == 0 and (stack[-1][0],stack[-1][1] + 1) in points:
				visited[stack[-1][0]][stack[-1][1] + 1] = 1
				stack.append((stack[-1][0],stack[-1][1] + 1))
				continue
			if visited[stack[-1][0] + 1][stack[-1][1] + 1] == 0 and (stack[-1][0] + 1,stack[-1][1] + 1) in points:
				visited[stack[-1][0] + 1][stack[-1][1] + 1] = 1
				stack.append((stack[-1][0] + 1,stack[-1][1] + 1))
				continue
			if visited[stack[-1][0] + 1][stack[-1][1]] == 0 and (stack[-1][0] + 1,stack[-1][1]) in points:
				visited[stack[-1][0] + 1][stack[-1][1]] = 1
				stack.append((stack[-1][0] + 1,stack[-1][1]))
				continue
			if visited[stack[-1][0] + 1][stack[-1][1] - 1] == 0 and (stack[-1][0] + 1,stack[-1][1] - 1) in points:
				visited[stack[-1][0] + 1][stack[-1][1] - 1] = 1
				stack.append((stack[-1][0] + 1,stack[-1][1] - 1))
				continue
			# if len(stack) >= 0.8 * size:
			# 	break
			if len(stack) >= 1:
				if (stack[-1][0] - 1,stack[-1][1] - 1) == minp or (stack[-1][0] - 1,stack[-1][1]) == minp or (stack[-1][0] - 1,stack[-1][1] + 1) == minp \
				or (stack[-1][0],stack[-1][1] - 1) == minp or (stack[-1][0],stack[-1][1] + 1) == minp or (stack[-1][0] + 1,stack[-1][1] - 1) == minp \
				or (stack[-1][0] + 1,stack[-1][1]) == minp or (stack[-1][0] + 1,stack[-1][1] + 1) == minp:
					break
			stack.pop()
			# if 任意一个方向中有一个是出发点且该集合不为空:
				# break
		while len(points) != 0:
			points.pop()
		while len(stack) != 0:
			points.append(stack.pop())			
	


	for points in inp:
		stack = []
		visited = [[0 for row in range(248)] for col in range(248)]
		size = len(points)
		# print(size)
		(maxp,minp) = find_x_range(points)
		stack.append(minp)
		visited[minp[0]][minp[1]] = 1
		# n = 0
		while True:
			# n+=1
			# print(len(stack))
			# 左上右下
			if visited[stack[-1][0]][stack[-1][1] - 1] == 0 and (stack[-1][0],stack[-1][1] - 1) in points:
				visited[stack[-1][0]][stack[-1][1] - 1] = 1
				stack.append((stack[-1][0],stack[-1][1] - 1))
				continue
			if visited[stack[-1][0] - 1][stack[-1][1] - 1] == 0 and (stack[-1][0] - 1,stack[-1][1] - 1) in points:
				visited[stack[-1][0] - 1][stack[-1][1] - 1] = 1
				stack.append((stack[-1][0] - 1,stack[-1][1] - 1))
				continue
			if visited[stack[-1][0] - 1][stack[-1][1]] == 0 and (stack[-1][0] - 1,stack[-1][1]) in points:
				visited[stack[-1][0] - 1][stack[-1][1]] = 1
				stack.append((stack[-1][0] - 1,stack[-1][1]))
				continue
			if visited[stack[-1][0] - 1][stack[-1][1] + 1] == 0 and (stack[-1][0] - 1,stack[-1][1] + 1) in points:
				visited[stack[-1][0] - 1][stack[-1][1] + 1] = 1
				stack.append((stack[-1][0] - 1,stack[-1][1] + 1))
				continue
			if visited[stack[-1][0]][stack[-1][1] + 1] == 0 and (stack[-1][0],stack[-1][1] + 1) in points:
				visited[stack[-1][0]][stack[-1][1] + 1] = 1
				stack.append((stack[-1][0],stack[-1][1] + 1))
				continue
			if visited[stack[-1][0] + 1][stack[-1][1] + 1] == 0 and (stack[-1][0] + 1,stack[-1][1] + 1) in points:
				visited[stack[-1][0] + 1][stack[-1][1] + 1] = 1
				stack.append((stack[-1][0] + 1,stack[-1][1] + 1))
				continue
			if visited[stack[-1][0] + 1][stack[-1][1]] == 0 and (stack[-1][0] + 1,stack[-1][1]) in points:
				visited[stack[-1][0] + 1][stack[-1][1]] = 1
				stack.append((stack[-1][0] + 1,stack[-1][1]))
				continue
			if visited[stack[-1][0] + 1][stack[-1][1] - 1] == 0 and (stack[-1][0] + 1,stack[-1][1] - 1) in points:
				visited[stack[-1][0] + 1][stack[-1][1] - 1] = 1
				stack.append((stack[-1][0] + 1,stack[-1][1] - 1))
				continue
			if len(stack) >= 1:
				if (stack[-1][0] - 1,stack[-1][1] - 1) == minp or (stack[-1][0] - 1,stack[-1][1]) == minp or (stack[-1][0] - 1,stack[-1][1] + 1) == minp \
				or (stack[-1][0],stack[-1][1] - 1) == minp or (stack[-1][0],stack[-1][1] + 1) == minp or (stack[-1][0] + 1,stack[-1][1] - 1) == minp \
				or (stack[-1][0] + 1,stack[-1][1]) == minp or (stack[-1][0] + 1,stack[-1][1] + 1) == minp:
					break
			if len(stack) > 0:
				stack.pop()
			# if 任意一个方向中有一个是出发点且该集合不为空:
				# break
		while len(points) != 0:
			points.pop()
		while len(stack) != 0:
			points.append(stack.pop())
	return (out,inp)

def outputployfiles(out,inp):
	f = open('a.ply', 'w')	
	f.write(str(len(out)+len(inp))+"\n")
	# f.write(str(len(out))+"\n")

	# 此处可能需要坐标转换
	for points in out:
		f.write(str(len(points))+' out\n')
		for point in points:
			f.write(str(point[0])+' '+(str(point[1]))+'\n')
		for i in range(1,len(points)+1):
			f.write(str(i)+' ')# 外边界顺时针
			# f.write(str(len(points)+1-i)+' ')
		f.write('\n')
	for points in inp:
		f.write(str(len(points))+' in\n')
		for point in points:
			f.write(str(point[0])+' '+(str(point[1]))+'\n')
		for i in range(1,len(points)+1):
			# f.write(str(i)+' ')
			f.write(str(len(points)+1-i)+' ')# 内边界逆时针
		f.write('\n')
	f.close()

def get_distance(point1,point2):
	return





if __name__ == 'main':
	time1 = time.time()

	print("start")
	f = open('./output_lux.txt')
	for i in range(248):
		graph.append(f.readline().split())
	for i in range(248):
		for j in range(248):
			graph[i][j] = (int)(graph[i][j])
	graph = np.array(graph)
	graph = pretreatment(graph)

	time2 = time.time()
	print(time2 - time1)
	(out,inp) = find_border(graph.shape[0],graph.shape[1])
	print(len(out),len(inp))
	(out,inp) = sort_incw(out,inp)
	print(len(out),len(inp))

	for points in out:
		for point in points:
			graph[point[0]][point[1]] += 200
		# print(len(points))

	# for points in inp:
		# print(len(points))

	n = 0
	for points in inp:
		n += 30
		# print(len(points))
		for point in points:
			graph[point[0]][point[1]] += n

	arr = np.array(graph)
	new_im = Image.fromarray(arr) 
	new_im.show()

	outputployfiles(out,inp)

	time3 = time.time()
	print(time3 - time2)
	# str = 'start ./acd2d_gui.exe a.ply'
	# p=os.system(str)