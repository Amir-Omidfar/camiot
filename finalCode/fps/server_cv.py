import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time

HOST='192.168.1.108'
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('Socket created')

s.bind((HOST,PORT))
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')

conn,addr=s.accept()

### new
counter=0
data = b''
payload_size = struct.calcsize("<L") 
while True:
    start=time.time()
    while len(data) < payload_size:
        data += conn.recv(8192)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("<L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(8192)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    ###

    frame=pickle.loads(frame_data)

    name='/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/fps/ft_data/frame'+str(counter)+'.jpg'
    cv2.imwrite(name,frame)
    counter+=1
    end=time.time()
    print("rate is: " ,end-start)

