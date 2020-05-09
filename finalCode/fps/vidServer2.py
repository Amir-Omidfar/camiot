
import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time

# ------------------------------------------ #
#           Server Client Interface          #
# ------------------------------------------ #
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.108', 8000))
server_socket.listen(0)

conn, addr = server_socket.accept()

data=b''
HEADERSIZE=512
#payload_size = struct.calcsize("L")
#print("L: ", payloa d_size)
#print("H: ",struct.calcsize("H"))

while True:
    full_data=b''
    new_data=True
    while True:
        begin=time.time()
        data=conn.recv(4096)
        if new_data:
            print("Here")
            print(f"new data length: {data[:HEADERSIZE]}")
            datalen= int(data[:HEADERSIZE])
            new_data=False

        full_data += data
        print("full data length: ",len(full_data))
        
        
        if len(full_data) == 4096:
            print("full data recevied: ")
            #print(full_data[HEADERSIZE:])
            halt=time.time() 
            print("rate is :" ,halt-begin)
            frame=pickle.loads(full_data[HEADERSIZE:])
            cv2.imshow('frame',frame)
            cv2.waitKey(.5)
            new_data=True
        #print(full_data)
        full_data=b''
        

	


'''
counter=0
while True:
    while len(data) < payload_size:
        data += conn.recv(1024)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    # print(data)
    msg_size = struct.unpack("package", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += conn.recv(1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    cv2.imshow('frame',frame)
    counter+= 1
    #conn.close()
'''
