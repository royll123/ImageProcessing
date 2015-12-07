import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from PIL import Image
import sys

average_filter = [	[float(1)/9, float(1)/9, float(1)/9],
					[float(1)/9, float(1)/9, float(1)/9],
					[float(1)/9, float(1)/9, float(1)/9]]

edge_filter = [	[0, 0, 0],
				[0, -1, 1],
				[0, 0, 0]]

rap_filter = [	[0, -1, 0],
				[-1, 5, -1],
				[0, -1, 0]]

def myfilter(image, h):
	width = image.shape[0]
	height = image.shape[1]
	new = np.array(image);
	for y in range(1, height-1):
		for x in range(1, width-1):
			point = 0
			for k in range(-1, 2):
				for l in range(-1,2):
					point += float(image[y+k][x+l])*h[k+1][l+1]
			new[y-1][x-1] = point
	img = Image.fromarray(np.uint8(new))
	img.show()

if len(sys.argv) == 2:
	img = Image.open(sys.argv[1]).convert('L')
	lgray = np.asarray(img, 'f')
	print lgray.shape
	img.show()
	myfilter(lgray, average_filter)
	myfilter(lgray, edge_filter)
	myfilter(lgray, rap_filter)
else:
	print "set image path"
