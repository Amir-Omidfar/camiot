import socket 
import time 

onMsg = "1"
offMsg = "0"

while True:
	userChoice = input ("Press 1 for the coffe maker and 2 for the printer ... \n")
	userChoice = int(userChoice)
	if (userChoice == 1):
		print("coffee maker selected")
		coffeClient = socket.socket()
		coffeClient.connect(('192.168.1.59',80))
		time.sleep(1)

		userInput = input("To turn ON press 1 or press 0 to turn OFF ... \n")
		userInput=int(userInput)
		if (userInput == 1):
			coffeClient.send(onMsg.encode())
			time.sleep(0.5)
			coffeClient.send(offMsg.encode())
			time.sleep(0.5)
			coffeClient.send(onMsg.encode())
			time.sleep(0.5)
			coffeClient.send(offMsg.encode())
			coffeClient.close()
		elif (userInput == 0):
			coffeClient.send(offMsg)
			coffeClient.close()

	elif (userChoice == 2):
		print("printer selected")
		printerClient = socket.socket()
		printerClient.connect(('192.168.1.27',80))
		time.sleep(1)

		userInput = input("To turn ON press 1 or press 2 to turn OFF ... \n")
		userInput=int(userInput)
		if (userInput == 1):
			printerClient.send(onMsg)
			printerClient.close()
		elif (userInput == 0):
			printerClient.send(offMsg)
			printerClient.close()
