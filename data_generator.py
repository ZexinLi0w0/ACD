import numpy as np

def data_generate(size,im,mlen,mhei):
	ls = list()
	for i in range(0,size):
		while 1:
			x = np.random.randint(0,mlen)
			y = np.random.randint(0,mhei)
			if(im[int(x)][int(y)] == 1):
				ls.append([x,y])
				break
	return ls