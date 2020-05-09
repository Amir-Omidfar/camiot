import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
import imutils
import time



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=False)
args = vars(ap.parse_args())

print("[INFO] starting video file thread...")
fvs = FileVideoStream(args["video"]).start()
time.sleep(1.0)

fps = FPS().start()

#cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.108',8089))


while True:
    while fvs.more():
        frame = fvs.read()
        data = pickle.dumps(frame) ### new code
        clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code
