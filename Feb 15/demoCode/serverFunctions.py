#Server code for demo May 6th 
import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time
import pyttsx3
engine = pyttsx3.init()
#TV, Printer, Lamp, CoffeeMaker, Toaster

##hard coded values for testing purposes 
resutls = dict([('TV',60),('Printer',20),('Lamp',10),('CoffeeMaker',5),('Toaster',5)])
resutls_list=['TV','Printer','Lamp','CoffeeMaker','Toaster']

def create_connection(HOST='192.168.1.108',PORT=8089):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print ('Socket created')
	s.bind((HOST,PORT))
	print ('Socket bind complete')
	s.listen(10)
	print ('Socket now listening')
	# Accpet the client 
	conn,addr=s.accept()
	print("connected to" ,addr)
	return s,conn,addr

def welcome_msg():
	engine = pyttsx3.init()
	engine.say('Hi, welcome to Camiot')
	engine.runAndWait()





def picRecv(thr,conn):
	counter=0
	data = b''
	payload_size = struct.calcsize("<L") 
	while counter < thr:
	    while len(data) < payload_size:
	        data += conn.recv(1024)
	    packed_msg_size = data[:payload_size]
	    data = data[payload_size:]
	    msg_size = struct.unpack("<L", packed_msg_size)[0]
	    while len(data) < msg_size:
	        data += conn.recv(1024)
	    frame_data = data[:msg_size]
	    data = data[msg_size:]
	    ###
	    frame=pickle.loads(frame_data)
	    name='/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/demoCode/data/frame'+str(counter)+'.jpg'
	    cv2.imwrite(name,frame)
	    print("saving image")
	    counter+=1
	return name


def detect_obj(conn):
	engine.say('Raise your arm to take a picture')
	engine.runAndWait()
	obj_img=picRecv(1,conn)
	'''
	Yuan's detection algorithm
	takes as input path to the image (obj_img)
	can be read using: cv.imread(obj_img)
	returns results as an ordered list 
	with the name of the appliances ordered 
	based on their classification prob  
	* using a hard coded one for now
	'''

	return state




def ask(obj, qnum): #ask for input from user using text input for now but can replace with the input from the camiot later
	print('qnum = ' + str(qnum))
	while True:
		if qnum == 1:
			choice = input('TV, Printer, Lamp, CoffeeMaker, Toaster, or q to terminate: ')
			break
		elif qnum == 2:
			choice = input("on, off, rechoose, repeat: ")
			break
		if obj == 'TV':
			if (qnum == 3): #volume or channel?
				choice = input("volume, channel, rechoose, repeat: ")
				break
			elif (qnum ==4):
				choice = input("up, down, rechoose, repeat: ")
				break
		elif obj == 'Printer':
			if qnum == 3:
				choice = input("print or rechoose for (on/off): ")
				break
		elif obj == 'Lamp':
			if qnum == 3:
				choice = input('bright, dark, or rechoose for (on/off): ')
				break
		elif obj == 'CoffeeMaker':
			if qnum == 3:
				choice = input('brew or rechoose for (on/off): ')
				break
		elif obj == 'Toaster':
			if qnum == 3:
				choice = input('toast or rechoose for (on/off): ')
				break
	return choice


def audio_interface():
#pass in a string that defines the object but for now we have the audio interface request the user to choose something. 
	engine = pyttsx3.init()
	while True:
		engine.say('Raise your arm to take a picture')
		engine.runAndWait()
		# Here goes the Yuan's alogrithm and print the results 

		obj = ask(None, 1)
		#input answer
		if obj == 'TV' or obj == 'Printer' or obj == 'Lamp' or obj == 'CoffeeMaker' or obj == 'Toaster':
			engine.say('You have chosen the '+obj)
			engine.runAndWait()
			while (True):
				qnum = 2
				engine.say('Please Point left for On, right for Off, up to choose the appliance again, or down to repeat the question')
				engine.runAndWait()
				choice = ask(obj, qnum) #input answer
				#execute this command
				qnum +=1

				if choice == "on":
					engine.say("Turning the " + obj + " on")
					engine.runAndWait()
					#execute this command
				elif choice == 'repeat':
					qnum -=1
					continue
				elif choice == 'rechoose':
					break
				else:
					engine.say('Shutting Down the ' + obj)
					engine.runAndWait()
					exit()
				if obj == 'TV':
						while(True):
							engine.say('Point left for Volume, right for Channel, up to choose on or off, or down to repeat the question')
							engine.runAndWait()
							choice = ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum -=1
								break 
							qnum += 1
							if choice == "volume":
								engine.say('You have chosen ' + choice)
								engine.runAndWait()
								while(True):
									engine.say('Point left for Volume Up, right for Volume Down, up to choose volume or channel, or down to repeat the question')
									engine.runAndWait()
									choice= ask(obj, qnum) 
									#execute answer
									if choice == 'rechoose':
										qnum -=1
										break
							elif choice == "channel":
								engine.say('You have chosen ' + choice)
								engine.runAndWait()
								while(True):
									engine.say('Point left for Channel Up, right for channel down, up to choose volume or channel, or down to repeat the question')
									engine.runAndWait()
									choice = ask(obj, qnum) 
									#execute answer
									if choice == 'rechoose':
										qnum-=1
										break
							elif choice == 'repeat':
								qnum -=1
								continue
							continue
						continue
				elif obj == 'Printer':
					while(True):
							engine.say('Point left to Print, right to choose on or off, or down to repeat the question')
							engine.runAndWait()
							choice = ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum -=1
								break 
							elif choice == 'print':
								engine.say('printing now')
								engine.runAndWait()
								#execute print job 
							elif choice == 'repeat':
								qnum -=1
								continue
					continue
				elif obj == 'Lamp':
					while(True):
							engine.say('Point left for brighter, right for darker, up to choose on or off, or down to repeat the question')
							engine.runAndWait()
							choice = ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum -=1
								break 
							elif choice == 'bright' or choice == 'dark':
								engine.say('Making the light ' + choice + 'er')
								engine.runAndWait()
								#execute command 
							elif choice == 'repeat':
								qnum -=1
								continue
					continue
				elif obj == 'CoffeeMaker':
					while(True):
							engine.say('Point left to brew coffee, right to choose on or off, or down to repeat the question')
							engine.runAndWait()
							choice = ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum -=1
								break 
							elif choice == 'brew':
								engine.say('Brewing coffee now')
								engine.runAndWait()
								#execute command 
							elif choice == 'repeat':
								qnum -=1
								continue
					continue
				elif obj == 'Toaster':
					while(True):
							engine.say('Point left to start toasting, right to choose on or off, or down to repeat the question')
							engine.runAndWait()
							choice = ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum -=1
								break 
							elif choice == 'toast':
								engine.say('Toasting now')
								engine.runAndWait()
								#execute command 
							elif choice == 'repeat':
								qnum -=1
								continue
					continue
		elif obj == 'q':
			exit()
		else:
			engine.say('Please choose a valid appliance')









