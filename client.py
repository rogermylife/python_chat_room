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
        global connected
        while True:
            try:
                data = self.sock.recv(BUFFER_SIZE)

                originData = data
                #print 'recv oringin '+originData
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
            
           
            elif data[0]=='sendfile':
                print '[sendfile] %s from %s' % (data[2],data[1])
                with open(data[2]+'_rev','wb') as recvFile:
                    recv = originData.replace('sendfile ','');
                    recv = recv.replace(data[1]+' ','');
                    recv = recv.replace(data[2]+' ','');
                    while recv.find(' %%%end%%%')==-1:
                        recv += self.sock.recv(BUFFER_SIZE)
                    print 'still recv?'
                    recv = recv.replace(' %%%end%%%','')
                    recvFile.write(recv)
            
            
            elif data[0]=='kick' and len(data)==2:
                print 'kick by '+data[1]
                connected=False
                self.sock.close()
                break;
            
            
            #print 'recv %s' % data
        print '[dissconnected]' 
        connected =False

    def kill(self):
        print 'stop'
        self.sock.close()
        os.kill(os.getpid(),9)

name = raw_input("Name:  ")


while True:
    global connected
    line = sys.stdin.readline()
    inputs = line.split()
    if not inputs:
        continue
    
    
    elif inputs[0]=='connect' :
        if len(inputs) !=3:
            print 'connect command error'
            continue
        print 'connecting...'
        if s != None and connected==True:
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
    
    
    elif inputs[0]=='sendfile' and len(inputs)==3:
        try:
            myFile = open(inputs[2],'rb')
        except:
            print 'no such file'
            continue;
        s.send('sendfile '+inputs[1]+' '+inputs[2]+' ')
        l = myFile.read(BUFFER_SIZE)
        while l:
            s.send(l)
            l=myFile.read(BUFFER_SIZE)
        s.send(' %%%end%%%')
        myFile.close()
    
    
    elif inputs[0]=='kick' and len(inputs)==2:
        s.send('kick '+inputs[1])


    elif inputs[0]=='exit()' and len(inputs)==1:
        recvThread.kill()
    
    
    else :
        print 'no this command'
