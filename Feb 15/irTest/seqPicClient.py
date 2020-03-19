import io
import socket
import struct
import time
import picamera
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.1.108', 8200))
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(36,GPIO.OUT,initial=GPIO.LOW)





camera = PiCamera(resolution=(480, 480), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
# Finally, take several photos with the fixed settings
camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])

'''
# Make a file-like object out of the connectio
connection = client_socket.makefile('wb')
try:
    with camera:
        # Start a preview and let the camera warm up for 2 seconds
        #GPIO.output(29,GPIO.LOW)
        #GPIO.output(36,GPIO.LOW)
        #camera.start_preview()
       # camera.exposure_mode = 'nightpreview'
        #time.sleep(2)

        start = time.time()
        timeelapsed = 0
        stream = io.BytesIO()
        for i in range(10):
            if i%2 == 1:
                GPIO.output(29,GPIO.HIGH)
                GPIO.output(36,GPIO.HIGH)
            starttime = time.time()
            camera.capture(stream , format='jpeg')
            stoptime = time.time()
            timeelapsed += stoptime - starttime
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
            GPIO.output(29,GPIO.LOW)
            GPIO.output(36,GPIO.LOW)

        print("Time of Image Capture = " +str(timeelapsed))
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()

'''




















