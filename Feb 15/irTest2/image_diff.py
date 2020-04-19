#https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/

import glob
import numpy as np
from skimage import filters
from skimage.measure import compare_ssim  
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt  
import FingerDetect 
from FingerDetect import fingerFinderFF



def masking(image,thre):
	output=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imshow("before Masking",output)
	#output=cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
	retval=cv2.threshold(output,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return retval,output


def fingerBottom(image): #pass in the flood filled image
	#get height and width of image
	height,width = image.shape
	

	white_thr = 230
	black_thr = 10
	counter=0
	counter_2=0
	left=0
	right=0
	thickness=0
	ls=0
	rs=0
	t=0
	w=470
	#print("height: ",height," width: ",width)
	#cv2.imshow("image",image)
	#print(image[w,:])
	#print(image[:,w])
	# get the white range for each line
	for j in range(width):
			 if image[w,j] >white_thr:
			 	if (counter_2==0):
			 		left=j
			 	elif (counter_2 > 0):
			 		right=j
			 		thickness=right-left
			 	counter_2=counter_2+1	
			 else:
			 	if (t<thickness):
			 		ls=left
			 		rs=right
			 		t=rs-ls
			 	left=0
			 	right=0
			 	counter=counter+1
			 	counter_2=0	
	midPixel=(rs+ls)/2
	return w,midPixel

def fingerBottomToTop(image):
	height,width = image.shape
	
	
	white_thr = 230
	counter=0
	left=0
	right=0
	thickness=0
	#left and right boundaries for scanning
	lb=0		
	rb=width-1
	ls=0
	rs=0
	t=0
	w=470
	midPixels=[]

	for i in range (0,height-10,10):
		for j in range(lb,rb,1):
			if image[w-i,j] > white_thr:
				if (counter==0):
					left=j
				elif (counter > 0):
					right=j
				counter=counter+1
			else:
				if(t<(right-left)):
					ls=left
					rs=right
					print("left ",left," right ",right, " counter", counter, "w-i " ,w-i, " j", j)
					t=rs-ls
				left=0
				right=0
				counter=0		
		midPixels.append((w-i,(rs+ls)/2))
		#lb=ls
		#rb=rs
		ls=0
		rs=0
		t=0	
		counter=0	
	#image[midPixels]=0
	#cv2.imshow*()		
	return midPixels	


	

	
def fignerFinder(image):
	#ap=argparse.ArgumentParser()
	#ap.add_argument("-f", "--first", required=True,help="first input image")
	#ap.add_argument("-s", "--second", required=True,help="second input image")
	#args = vars(ap.parse_args())
	#setting the threshold value in case we use cv2.THRESH_BINARY
	thre=200
	radius=101


	#load the image 
	#ir=cv2.imread(image)	
	ir=image
	#noIr=cv2.imread(args["second"])
	#apply different thresholding so far gussian and adaptive means are better  
	#irRet,irOut=masking(ir,thre)
	#noirRet,noIrOut=masking(noIr,thre)

	#cv2.imwrite("results/irOut_ADAPTIVE_THRESH_MEAN.jpg",irOut)
	#cv2.imwrite("results/noIrOut_ADAPTIVE_THRESH_MEAN.jpg",noIrOut)
	retval,irG=masking(ir,thre)
	cv2.imshow("masked" ,irG)
	cv2.waitKey(0)
	bx,by=fingerBottom(irG)
	by=int(by)
	#print(bx)
	#print(by)
	#bottom=(bx,int(by)
	irG = cv2.GaussianBlur(irG, (radius, radius), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(irG)
	cv2.arrowedLine(ir, (by,bx), maxLoc, (0,0,255),2)
	return ir 
	'''
	h,w=irG.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(ir, mask,(0,0), 255)
	ir_inv = cv2.bitwise_not(ir)
	ir_out=ir && ir_inv
	#cv2.imshow("arrowDirection",ir)
	cv2.imshow("FloodFill",ir)
	cv2.imshow("inv added",ir_out)
	'''
	#cv2.imshow("test",ir)
	#cv2.waitKey(0)
	# find the white area of the finger 


def batchTest():
	images = [cv2.imread(file) for file in glob.glob("fingerData/exp2/*.jpg")]

	count=1

	for i in images:
		cv2.imwrite("results/exp2/ff/"+str(count)+"ff.jpg",fingerFinderFF(i))
		#cv2.imwrite("results/exp2/noFF/"+str(count)+"Noff.jpg",fignerFinder(i))
		count=count+1




image=cv2.imread("fingerData/exp2/75.jpg")

gray=output=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binaryImage=cv2.threshold(image,230,255,cv2.THRESH_BINARY)
cv2.imshow("binaryImage", binaryImage)
#fignerFinder(image)
midPixels=fingerBottomToTop(gray)
print(midPixels)
cv2.arrowedLine(gray, (238,470), (279,370), (0,0,255),2)
cv2.imshow("line",gray)
cv2.waitKey(0)



	
