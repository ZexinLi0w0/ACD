f = open('copy_a.ply')
g = open('asd.ply','w')
lines = (f.readline().split())[0]
lines = (int)(lines)
g.write(str(lines))
print(lines)
for i in range(lines):
	list = f.readline().split()
	print(list)
	g.write(str(lines))
	for j in range((int)(list[0])):
		g.write((str)(f.readline()))
	for j in range((int)(list[0])):
		g.write(str((int)(list[0]) - 1 - j)+' ')
	g.write('\n')
g.close()
f.close()
