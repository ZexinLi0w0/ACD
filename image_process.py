from  PIL import Image
import matplotlib.image as plimg
import matplotlib.pyplot as plt

def read_image(filepath, ratio):
	im = Image.open(filepath)
	(length,height) = im.size
	im = im.resize((length//ratio,height//ratio))
	print(im)
	# im.save('cymsbsbsbsb.png')
	imarr = plimg.pil_to_array(im)
	imarr.flags.writeable = True
	graph_normalization(imarr,length//ratio,height//ratio)
	return (imarr,length//ratio,height//ratio)


def graph_normalization(imarr,length,height):
	for i in range(length):
		for j in range(height):
			if imarr[i][j] == 254:
				imarr[i][j] = 1
			else:
				imarr[i][j] = 0
