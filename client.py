#!/usr/bin/env python

import socket
import sys
import os
from threading import Thread

ip = ''
port = 9001
BUFFER_SIZE = 1024
s = None
recvThread = None
connected = False

class RecvThread(Thread):

    def __init__(self,ip,port,sock,name):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.name = name
        #print " New thread started for "+ip+":"+str(port)
        print 'successfully connect %s:%s' % (inputs[1],inputs[2])

    def run(self):
        while True:
            try:
                data = self.sock.recv(BUFFER_SIZE)
                data = data.split()
            except:
                print '%s:%s connection closed' % (self.ip,self.port)
                break
            
            
            if data[0]=='list':
                for i in range (1,len(data)):
                    if data[i]=='%%%end%%%':
                        break;
                    print data[i]
            
            
            elif data[0]=='chat' and len(data)==3:
                print '[chat] from %s : %s' % (data[1],data[2])
            
            
            print 'recv %s' % data
    def kill(self):
        print 'stop'
        self.sock.close()
        os.kill(os.getpid(),9)

name = raw_input("Name:  ")


while True:
    line = sys.stdin.readline()
    inputs = line.split()
    if not inputs:
        continue
    
    
    elif inputs[0]=='connect' :
        if len(inputs) !=3:
            print 'connect command error'
            continue
        print 'connecting...'
        if s != None:
            #print 'close ex'
            s.send("exit()")
            s.close()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((inputs[1],int(inputs[2])))
            ip = inputs[1]
            port = int(inputs[2])
            s.send(name)
            recvThread = RecvThread(ip,port,s,name)
            recvThread.start()
            connected=True
        except socket.error,msg:
            print 'socket error %s' % msg
            connected=False

    
    elif not connected:
        print 'please connect first'
        continue
    
    
    elif inputs[0]=='list' and len(inputs)==1:
        s.send('list')
    
    
    elif inputs[0]=='chat' and len(inputs)==3:
        s.send('chat '+inputs[1]+' '+inputs[2])
    
    
    elif inputs[0]=='exit()':
        recvThread.kill()
    
    
    else :
        print 'no this command'

s.connect((TCP_IP, TCP_PORT))
with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print 'file close()'
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
print('connection closed')
