import math
import copy
import cv2
import queue
import time
import os
from PIL import Image
import numpy as np

graph = []

def initialize(new_graph):
	global graph
	graph = pretreatment(new_graph)
	(minx_point,maxx_point) = find_x_range(new_graph)
	(out_border,in_border) = find_border(graph.shape[0],graph.shape[1])
	path = []
	path.append(minx_point)
	path.append(maxx_point)
	# for points in in_border:
	# 	(temp_border_list,temp_point_list) = cut_to_convex(points)
	# 	for border in temp_border_list:
	# 		path.append(find_core(border))
	# sorted(path,key=lambda x: x[0])
	# border_graph1 = ...
	# border_graph2 = ...
	# (temp_border_list_1,temp_point_list_1) = cut_to_convex(graph1)
	# (temp_border_list_2,temp_point_list_2) = cut_to_convex(graph2)
	# for border in temp_border_list_2:
	# 	temp_border_list_1.append(border)
	# for points in temp_point_list_2:
	# 	temp_point_list_1.append(points)
	# return (temp_border_list_1,temp_point_list_1)
	return path

	# randompoint = get_randompoint(border_list)
	# border_list = find_border(graph.shape[0],graph.shape[1])
	# vertex_list = find_vertex(border_list,graph.shape[0],graph.shape[1])
	# convex_to_points = find_mapping(graph,vertex_list)

# def get_randompoint(list):
# 	(x,y) = (np.random.randint(192), np.random.randint(192))
# 	while not graph[x][y] or not minsquare_distance_to_graph(x,y,list) > 100:
# 		(x,y) = (np.random.randint(192), np.random.randint(192))
# 	return (x,y)

# def minsquare_distance_to_graph(x,y,list):
# 	dis = 1e10
# 	for point in list:
# 		dis = dis if (x - point[0]) * (x - point[0]) + (y - point[1]) * (y - point[1]) > dis else (x - point[0]) * (x - point[0]) + (y - point[1]) * (y - point[1])
# 	return dis
	
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
	minx_point = (192,192)
	maxx_point = (0,0)
	for point in list:
		if point[0] < minx_point[0]:
			minx_point = (point[0],point[1])
		if point[0] > maxx_point[0]:
			maxx_point = (point[0],point[1])
	
	return (minx_point,maxx_point)

def find_border(row,column):
	list = []
	for i in range(row):
		for j in range(column):
			if graph[i][j] == 1:
				temp = count(i,j)
				if temp < 8 and temp > 0:
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
		visited = [[0 for row in range(192)] for col in range(192)]
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
		visited = [[0 for row in range(192)] for col in range(192)]
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
			# f.write(str(i)+' ')
			f.write(str(len(points)+1-i)+' ')
		f.write('\n')
	for points in inp:
		f.write(str(len(points))+' in\n')
		for point in points:
			f.write(str(point[0])+' '+(str(point[1]))+'\n')
		for i in range(1,len(points)+1):
			# f.write(str(i)+' ')
			f.write(str(len(points)+1-i)+' ')
		f.write('\n')
	f.close()








# def find_core(list):
# 	count = 0
# 	x = 0
# 	y = 0
# 	for point in list:
# 		count += 1
# 		x += point[0]
# 		y += point[1]
# 	x //= count
# 	y //= count
# 	return (x,y)





# def cut_to_convex(list):
# 	list = border
# 	border_list = []
# 	point_list = []
# 	for points in border:
# 		temp_border = []
# 		temp_point = []
# 		while not len(points) == 0:
			

# 		list.remove(points)
# 		border_list.append(temp_border)
# 		point_list.append(temp_point)

# 	return (border_list,point_list)



# def from_border_to_allpoints(list):
# 	visited = [[0 for row in range(192)] for col in range(192)]
# 	q = queue.Queue()
# 	store = []
# 	temp_graph = [[0 for row in range(192)] for col in range(192)]

# 	(x,y) = find_core(list)
# 	q.put((x,y))
# 	visited[x][y] = 1

# 	for point in list:
# 		temp_graph[point[0]][point[1]] = 1

# 	while not q.empty():
# 		temp = q.get()
# 		store.append(temp)
# 		if visited[temp[0] - 1][temp[1]] == 0 and temp_graph[temp[0] - 1][temp[1]] == 0:
# 			q.put((temp[0] - 1,temp[1]))
# 			visited[temp[0] - 1][temp[1]] = 1
# 		if visited[temp[0] + 1][temp[1]] == 0 and temp_graph[temp[0] + 1][temp[1]] == 0:
# 			q.put((temp[0] + 1,temp[1]))
# 			visited[temp[0] + 1][temp[1]] = 1
# 		if visited[temp[0]][temp[1] - 1] == 0 and temp_graph[temp[0]][temp[1] - 1] == 0:
# 			q.put((temp[0],temp[1] - 1))
# 			visited[temp[0]][temp[1] - 1] = 1
# 		if visited[temp[0]][temp[1] + 1] == 0 and temp_graph[temp[0]][temp[1] + 1] == 0:
# 			q.put((temp[0],temp[1] + 1))
# 			visited[temp[0]][temp[1] + 1] = 1
# 		if visited[temp[0] - 1][temp[1] - 1] == 0 and temp_graph[temp[0] - 1][temp[1] - 1] == 0:
# 			q.put((temp[0] - 1,temp[1] - 1))
# 			visited[temp[0] - 1][temp[1] - 1] = 1
# 		if visited[temp[0] - 1][temp[1] + 1] == 0 and temp_graph[temp[0] - 1][temp[1] + 1] == 0:
# 			q.put((temp[0] - 1,temp[1] + 1))
# 			visited[temp[0] - 1][temp[1] + 1] = 1
# 		if visited[temp[0] + 1][temp[1] - 1] == 0 and temp_graph[temp[0] + 1][temp[1] - 1] == 0:
# 			q.put((temp[0] + 1,temp[1] - 1))
# 			visited[temp[0] + 1][temp[1] - 1] = 1
# 		if visited[temp[0] + 1][temp[1] + 1] == 0 and temp_graph[temp[0] + 1][temp[1] + 1] == 0:
# 			q.put((temp[0] + 1,temp[1] + 1))
# 			visited[temp[0] + 1][temp[1] + 1] = 1
	
# 	for point in list:
# 		store.append(point)

# 	return store
# 	# return temp_graph1

def get_distance(point1,point2):
	return






time1 = time.time()
print("start")
f = open('./out3.txt')
for i in range(192):
	graph.append(f.readline().split())

for i in range(192):
	for j in range(192):
		graph[i][j] = (int)(graph[i][j])

graph = np.array(graph)

# (tborder,tpoints) = initialize(graph)
# for i in range(192):
# 	for j in range(192):
# 		graph[i][j] *= 50

graph = pretreatment(graph)
# (minx_point,maxx_point) = find_x_range(graph)
# print((minx_point,maxx_point))
time2 = time.time()
print(time2 - time1)



(out,inp) = find_border(graph.shape[0],graph.shape[1])

print(len(out),len(inp))
# (out,inp) = sort_incw(out,inp)
# out = sort_incw(out,inp)
print(len(out),len(inp))
out1 = []
# for points in out:
# 	for point in points:
# 		graph[point[0]][point[1]] += 50
# 	print(len(points))

(out,inp) = sort_incw(out,inp)
# 返回内外边界
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
		out1.append((point[0],point[1]))

arr = np.array(graph)

new_im = Image.fromarray(arr) 
new_im.show()

outputployfiles(out,inp)

time3 = time.time()
print(time3 - time2)

str = 'test.bat'
p=os.system(str)