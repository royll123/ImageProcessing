import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from PIL import Image
import sys
import math

average_filter = [      [float(1)/9, float(1)/9, float(1)/9],
                        [float(1)/9, float(1)/9, float(1)/9],
                        [float(1)/9, float(1)/9, float(1)/9]]

edge_filter = [	[0, 0, 0],
                [0, -1, 1],
                [0, 0, 0]]

rap_filter = [	[0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]]

dither_bayer = [    [0, 8, 2, 10],
                    [12, 4, 14, 6],
                    [3, 11, 1, 9],
                    [15, 7, 13, 5]]

def medianFilter(image, n, m):
    width = image.shape[0]
    height = image.shape[1]
    tmp = np.array(image)
    for y in range(n/2, height-n/2):
        for x in range(m/2, width-n/2):
            box = image[y-n/2:y+n/2+1]
            items = []
            for i in box:
                for j in i[x-m/2:x+m/2+1]:
                    items.append(j)
            items.sort()
            tmp[y][x] = items[n*m/2]
    img = Image.fromarray(np.uint8(tmp))
    img.show()

def calc_bilateral_w(image, width, height, w, sig1, sig2):
    wary = np.empty([width, height, 2*w+1, 2*w+1], dtype=np.float)
    for j in range(0, height-w):
        for i in range(0, width-w):
            for m in range(-w, w+1):
                for n in range(-w, w+1):
                    wary[i][j][m+w][n+w] = calc_bilateral_w2(image[j][i], image[j+m][i+n], m, n, sig1, sig2)
    return np.copy(wary)

def calc_bilateral_w2(fij, fmn, m, n, sig1, sig2):
    return math.exp(-(m*m+n*n)/(2*sig1*sig1))*math.exp(-(fij-fmn)*(fij-fmn)/(2*sig2*sig2))

def bilateralFilter(image, w, sig1, sig2):
    width = image.shape[0]
    height = image.shape[1]
    tmp = np.array(image)
    #wary = calc_bilateral_w(image, width, height, w, sig1, sig2)
    for y in range(w, height-w):
        for x in range(w, width-w):
            top = 0.0
            bottom = 0.0
            for n in range(-w, w+1):
                for m in range(-w, w+1):
                    wc = calc_bilateral_w2(image[y][x], image[y+m][x+n], m, n, sig1, sig2);
                    top += wc*image[y+m][x+n]
                    bottom += wc;
                    #top += wary[x][y][m+w][n+w]*image[y+m][x+n]
                    #bottom += wary[x][y][m+w][n+w]
            tmp[y][x] = top/bottom
            print tmp[y][x], image[y][x]
    img = Image.fromarray(np.uint8(tmp))
    img.show()
    return img

def ditherFilter(image, ditherPattern):
    width = image.shape[0]
    height = image.shape[1]
    tmp = np.array(image)
    for y in range(0, height/4):
        for x in range(0, width/4):
            for j in range(0, 4):
                for i in range(0, 4):
                    if image[y*4+j][x*4+i] >= ditherPattern[j][i]*16+8:
                        tmp[y*4+j][x*4+i] = 255
                    else:
                        tmp[y*4+j][x*4+i] = 0
    img = Image.fromarray(np.uint8(tmp))
    img.show()
    return img

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

if __name__ == "__main__":
    if len(sys.argv) == 2:
        img = Image.open(sys.argv[1]).convert('L')
        lgray = np.asarray(img, 'f')
        img.show()
    #   myfilter(lgray, average_filter)
    #   myfilter(lgray, edge_filter)
    #   myfilter(lgray, rap_filter)
    #   medianFilter(lgray, 3, 3)
        img = bilateralFilter(lgray, 5, 2, 1)
        bilateralFilter(img, 5, 2, 1)
        ditherFilter(lgray, dither_bayer)
    else:
        print "set image path"
