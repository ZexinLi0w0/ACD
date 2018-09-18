from PIL import Image, ImageDraw
import numpy as np

im = Image.open("a.pgm")
im = im.convert('RGB')

(length,height) = im.size
im = im.resize((length//2,height//2))

draw = ImageDraw.Draw(im)
# draw.line((0, 0) + im.size, fill=128)

# draw = ImageDraw.Draw(im)
# draw.line((ax,ay,bx,by),fill=color)


# write to stdout
# im.save(sys.stdout, "PNG")


ans1 = [[86, 103, 5], [86, 110, 15], [86, 117, 26], [88, 122, 36], [71, 133, 47], [81, 143, 58], [110, 149, 69], [121, 157, 80], [146, 165, 91], [98, 165, 102], [82, 169, 114], [63, 157, 126], [58, 158, 137], [47, 170, 148], [49, 154, 159], [60, 146, 169], [53, 146, 179], [53, 143, 188], [47, 131, 197], [65, 120, 206], [66, 117, 215], [67, 93, 224], [67, 87, 233], [71, 76, 242], [55, 89, 252], [53, 98, 261], [42, 90, 271], [40, 86, 280], [44, 80, 289], [47, 74, 298], [58, 60, 307], [56, 59, 315], [49, 53, 324], [48, 46, 333], [44, 35, 342], [65, 40, 352], [70, 36, 361], [70, 39, 370], [75, 44, 379], [82, 30, 389], [89, 35, 399], [91, 25, 409], [117, 25, 419], [120, 38, 430], [104, 37, 440], [91, 56, 451], [80, 53, 462], [88, 73, 473], [92, 86, 484], [92, 94, 494]]
ans = []
for point in ans1:
	point.pop()
for point in ans1:
	tl = []
	for x in point:
		# tl.append(2*x)
		tl.append(x)
	ans.append(tl)	
temp = 0
while temp < len(ans)-1:
# while temp < 18:
	draw.line((ans[temp][1],ans[temp][0],ans[temp+1][1],ans[temp+1][0]),fill=(255,0,0))
	temp += 1
draw.line((ans[temp][1],ans[temp][0],ans[0][1],ans[0][0]),fill=(255,0,0))
print(ans)
flatten = []
for point in ans:
	for x in point:
		flatten.append(x)

print(len(flatten))
t = 0
nw = []
while t < len(flatten) - 1:
	nw.append((flatten[t+1],flatten[t]))
	t += 2
print(nw)
draw.point(nw, fill=(255,0,0))
# im.save('only.png')
# im.save('only point.png')
arr = np.array(im)
print(arr[42][99])
im.save('path.png')
# print(ans)