	#Server code for demo May 6th 


'''
while True:
	1. trigger mechanism for taking pic (client)
	2. process the pic and announce the result (server)
	3-a. if it's the desired item wait 2 sec to enter the next loop
	3-b. othewise toggle through the possible options until the desired option
		
	--> printer(80) coffee maker(10%) tv(10%) ....	(try toggle )
		use twisting gesture for confirming the selection or for toggling in the menu
	detection block (Yuan's algo) (takes on image, return as above )

	4. Enter finger interaction by taking pics continously
		finger intearction algo (input : take images in while looop as fast as possible)
			audio feedback for the user to confirm his gesture, drop the finger if they are happy with the results 
	5. Process the pics and say the result   
	6. Given the appliance matches the direction detected to the function avaliable

	# Server side 
	1. appliance detection algorithm
	2. finger detection algorithm
	3. voice command implementation in both algorithms 

	# Client side
	1. Trigger
	2. take and send picture

'''
#Server code for demo May 6th 
import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time
import pyttsx3
import serverFunctions
from serverFunctions import *
from engine_simple_infer_STANDARD_VGG_classification import appliance_recognition
from engine_simple_infer_STANDARD_VGG_classification import *
# voice command init
engine = pyttsx3.init()
# 0= object detection 1=finger interaction
state = 0








#Make a connection with the client
s,conn,addr=create_connection()
#wait until the connection is created
welcome_msg()
#result_prob, result_items=appliance_recognition('/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/demoCode/test_Img/lamp_right.jpg')
#print(result_prob)
#print(result_items)
conn.send(1.encode())

while True :
	#start with detection algo
	if (state == 0):	print ('Socket bind complete')

		imgName=picRecv(1,conn)
		result_prob, result_items=appliance_recognition(imgName)





	












