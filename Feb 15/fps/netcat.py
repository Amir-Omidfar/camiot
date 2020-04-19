import sys
import socket
hostname='192.168.1.108'
port=8200

def netcat(hn,p):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((hn,p))

netcat(hostname,port)


