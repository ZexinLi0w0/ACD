# Description
This program is used to generate proper path for autonomatic driving. Since path can not 
be simplified as skelton in this program, we need to do 2D approximately convex 
decomposition. (This part comes from https://github.com/jmlien/acd2d) After ACD, we use 
SOM alogrithm to generate path for TSP and MTSP problem.

print_image.py: print solution to 'only_point.png' and 'path.png'
main.py:You should input cities list in a list which contains all city postion in the \
following way:[double/int:pos_x,double/int:pos_y], and after computing you will get a \
sorted list which represents the order of cities in the following way: \
[double/int:pos_x, double/int:pos_y, double/int:key].

# Test
Just `python main.py`

# License
MIT license

# Acknowledge
Refer to https://github.com/jmlien/acd2d
Thanks for Yiming Chen's support
