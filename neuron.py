import numpy as np

def init_network(size,im,mlen,mhei):
	ls = list()
	for i in range(0,size):
		while 1:
			x = np.random.uniform(0,mlen)
			y = np.random.uniform(0,mhei)
			if(im[int(x)][int(y)] == 1):
				ls.append(np.array([x,y]))
				break
	return np.array(ls)


def get_neighborhood(center, radix, domain):
    if radix < 1:
        radix = 1
    deltas = np.absolute(center - np.arange(domain))
    distances = np.minimum(deltas, domain - deltas)
    return np.exp(-(distances*distances) / (2*(radix*radix)))