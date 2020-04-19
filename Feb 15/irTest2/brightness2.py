import numpy as np
from skimage import filters
from skimage.measure import compare_ssim  
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt  



def image_bright():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help = "path to the image file")
	ap.add_argument("-r", "--radius", type = int,
		help = "radius of Gaussian blur; must be odd")
	args = vars(ap.parse_args())
	# load the image and convert it to grayscale

	image = cv2.imread(args["image"])
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# perform a naive attempt to find the (x, y) coordinates of
	# the area of the image with the largest intensity value
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)
	# display the results of the naive attempt
	cv2.imshow("Naive", image)
	# apply a Gaussian blur to the image then find the brightest
	# region
	gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	cv2.imshow("Grayscale", gray)
	image = orig.copy()
	cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)
	# display the results of our newly improved method
	cv2.imshow("Robust", image)
	cv2.waitKey(0)




image_bright()