from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time
#from training import classifier
from joblib import dump,load
import numpy as np

classifier = load ('/home/pi/Desktop/trigger/triggerTrain26-2.joblib')

def trigger():
  imuData = open("imuPredictData.csv","a")
  
  active = True
  counter = 0
  label = ""
  data= []
  print("Recording Data")
  while active:
        '''
        imuData.write("\n")
        imuData.write(label)
        imuData.write(", ")
        imuData.write(str(counter))
        imuData.write(", ")
        startTime=time.time()
        '''
        while len(data) < 84 : 
            accel_data = sensor.get_all_data()[0]
            gyro_data = sensor.get_all_data()[1]
  
            data.append(accel_data['x'])
            data.append(accel_data['y'])
            data.append(accel_data['z'])
            
            data.append(gyro_data['x'])
            data.append(gyro_data['y'])
            data.append(gyro_data['z'])
            
            time.sleep(0.1)
        #data.pop()
        #data.pop()
        #data.pop()
        #data.pop()
        #data.pop()
        #data.remove(data[0])
        #print("Initial shape of data: " ,len(data))
        newData=np.reshape(data,(1,-1))
        #print("new Size ",newData.shape)
        result = classifier.predict(newData)
        #print(result)
        if result:
            print("True")
            return True
        
        for k in range(18):
          data.pop(0)
        #data.clear()

#while True:
 # imuTri()
#imuTri()
