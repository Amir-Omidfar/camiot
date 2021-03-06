import socket
import subprocess
from subprocess import check_output
import cv2

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.1.108', 8200))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    #cmdline = ['vlc', '--demux', 'h264', '-']
    
    #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    #player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
            break
        print("the data len is :" ,len(data))
        #player.stdin.write(data)
        currentFrame=0
        while currentFrame < len(data):
            name='/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/fps/data/frame'+str(currentFrame)+'.jpg'
            print('Creating ...' + name)
            cv2.imwrite(name,data[currentFrame])
            currentFrame+=24

finally:
    connection.close()
    server_socket.close()
    #player.terminate()
