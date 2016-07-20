# -*- coding: utf-8 -*-
import socket

#clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket = socket.socket()

host = socket.gethostname()
port = 5566

clientSocket.connect((host,port))
clientSocket.send('Hello server!')

with open('received_file','wb') as received_file:
    print 'file opened'
    while True:
        print('receiving data...')
        data = clientSocket.recv(1024)
        print('data=%s' % (data))
        if not data:
            break
        received_file.write(data)

received_file.close()
print('Successfully get the file')
#tm = clientSocket.recv(1024)
#tm = '天ㄚ  寫的完嘛?'

clientSocket.close()

print("connection closed" )
#print("The time got from the server is %s and My host is %s" % (tm.decode('utf-8'),str(host)) )
