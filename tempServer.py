# -*- coding: utf-8 -*-
import socket 
import time

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
port = 5566 

serverSocket.bind((host,port))

serverSocket.listen(5)

while True:
    clientSocket,addr = serverSocket.accept()
    print("Got a connection from %s" % (str(addr)) )
    data = clientSocket.recv(1024)
    print('Server received',repr(data))
    fileName = 'myText.txt'
    myFile = open(fileName,'rb')
    l = myFile.read(1024)
    while l:
        clientSocket.send(l)
        print('Sent ',repr(l))
        l = myFile.read(1024)
    myFile.close()
    
    
    #currentTime = time.ctime(time.time()) + "\r\n"
    #string = '天天天天ㄚ 許功蓋'
    #clientSocket.send(string)
    print('Done sending')
    clientSocket.send('connection close')
    clientSocket.close()
