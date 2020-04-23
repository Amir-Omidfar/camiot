#Here goes the client code 

import cv2
import numpy as np
import socket
import pickle
import struct ### new code

import sys
sys.path.insert(1, '/trigger/')

from testImuCon import trigger 

state=0 # 0= object detection 1=finger interaction

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.108',8089))

state=clientsocket.recv().decode
print(state)

while True:

	if state ==0:	
		if trigger():
    		ret,frame=cap.read()
    		data = pickle.dumps(frame) ### new code
    		clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code
