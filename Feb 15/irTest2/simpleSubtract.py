import numpy as np
import cv2 
# import the necessary packages
from skimage import measure
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2





orig=cv2.imread("noIr.jpg")
ir=cv2.imread("ir.jpg")

sub=cv2.subtract(orig,ir)
cv2.imshow("sub",sub)
origG=cv2.cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
irG=cv2.cv2.cvtColor(ir, cv2.COLOR_BGR2GRAY)
cv2.imshow("origG",origG)
cv2.imshow("irG",irG)
subG=cv2.subtract(irG,origG)
cv2.imshow("subG",subG)
cv2.waitKey(0)
#irFloodFill=cv2.FloodFill(ir, seed_point, 255, lo_diff=(0, 0, 0, 0), up_diff=(0, 0, 0, 0), flags=4, mask=None)


'''
subOI=orig-ir
subIO=ir-orig
cv2.imshow("orig",orig)
cv2.imshow("orig-ir",subOI)
cv2.imshow("ir-orig",subIO)
cv2.waitKey(0)
#gray=cv2.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray",gray)

gray=cv2.cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
'''
'''
height,width=gray.shape
result=np.zeros([height, width], dtype=np.uint8)
for i in range(height):
	for j in range(width):
		if (orig[i,j] == subOI[i,j]):
			result[i,j]=255
		else:
			result[i,j]=0
cv2.imshow("result",result)
cv2.waitKey(0)
'''
