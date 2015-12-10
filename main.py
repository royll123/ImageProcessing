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

def medianFilter(image, n, m):
	width = image.shape[0]
	height = image.shape[1]
	tmp = np.array(image)
	for y in range(n, height-n):
		for x in range(m, width-n):
			box = image[y-n/2:y+n/2+1]
			items = []
			for i in box:
				for j in i[x-m/2:x+m/2+1]:
					items.append(j)
			items.sort()
			print items
			tmp[y][x] = items[n*m/2]

	img = Image.fromarray(np.uint8(tmp))
	img.show()

def myfilter(image, h):
	width = image.shape[0]
	height = image.shape[1]
	new = np.array(image)
	maxi = -1
	mini = 256
	for y in range(1, height-1):
		for x in range(1, width-1):
			point = 0
			for k in range(-1, 2):
				for l in range(-1,2):
					point += float(image[y+k][x+l])*h[k+1][l+1]
			if point > maxi:
				maxi = point
			if point < mini:
				mini = point
			if point < 0:
				point = 0
			if point > 255:
				point = 255
			new[y-1][x-1] = point
#	if maxi > 255 or mini < 0:
#		if maxi > 255:
#			diff = maxi - 255
#		elif mini < 0:
#			diff = mini
#		for y in range(1, height-1):
#			for x in range(1, width-1):
#				if new[y-1][x-1] < 0 or new[y-1][x-1] > 255:
#					new[y-1][x-1] -= diff
	
	img = Image.fromarray(np.uint8(new))
	img.show()

if len(sys.argv) == 2:
	img = Image.open(sys.argv[1]).convert('L')
	lgray = np.asarray(img, 'f')
	print lgray.shape
	img.show()
#	myfilter(lgray, average_filter)
#	myfilter(lgray, edge_filter)
#	myfilter(lgray, rap_filter)
	medianFilter(lgray, 3, 3)
else:
	print "set image path"
