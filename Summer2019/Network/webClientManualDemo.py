import socket 
import time 


onMsg = "1"
offMsg = "0"

applianceDict= {
	1 : ("Coffee Maker","192.168.1.7"),
	2 : ("TV","192.168.1.63"),
	3 : ("Printer","192.168.1.64"),
	4 : ("PC","192.168.1.61"),
	5 : ("Door","192.168.1.62"),
	6 : ("Lamp","192.168.1.59"),
}

def callAppliace(appliaceName,ipAddr):
	print(appliaceName,"is selected")
	appliaceClient=socket.socket()
	appliaceClient.connect((ipAddr,80))
	time.sleep(1)
	return appliaceClient

def controlAppliance(appliaceClient):
	userInput = input("To turn ON press 1 or press 0 to turn OFF ... \n")
	userInput=int(userInput)
	if (userInput == 1):
		appliaceClient.send(onMsg.encode())
		appliaceClient.close()
	elif (userInput == 0):
		appliaceClient.send(offMsg.encode())
		appliaceClient.close()


while True:
	userChoice = input ("Select your appliance: \n 1 for Coffe Maker \n 2 for TV \n 3 for Printer \n 4 for PC \n 5 for Door \n 6 for Lamp...\n")
	userChoice = int(userChoice)
	if userChoice in applianceDict:
		applianceTuple=applianceDict[userChoice]
		applianceClient=callAppliace(applianceTuple[0],applianceTuple[1])
		controlAppliance(applianceClient)