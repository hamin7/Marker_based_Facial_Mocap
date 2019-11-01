import os
import socket
import subprocess

s = socket.socket()
host = '166.104.29.148'
#host = '192.168.0.7'
port = 7777
s.connect((host,port))

while True:
    Val = input("send: ").encode()
    s.send(Val)
    
s.close()

#http://creativeworks.tistory.com/
