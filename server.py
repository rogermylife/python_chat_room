import socket
import time
from threading import Thread
from SocketServer import ThreadingMixIn


TCP_IP = '188.166.241.205'
TCP_PORT = 9001
BUFFER_SIZE = 1024
onlineUsers = [(None,'')]
class ClientThread(Thread):

    def __init__(self,ip,port,sock,name):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.name = name
        onlineUsers.append((self.sock,self.name))
        print "[login] "+name+" from "+ip+":"+str(port)

    def run(self):
        global onlineUsers
        while True:
            try:
                data = self.sock.recv(BUFFER_SIZE)
                originData = data
                print self.name+': recv origin   '+originData;
                data = data.split()
                test = data[0]
            except IndexError:
                #print '[logout1] %s from %s:%s' % (self.name,self.ip,self.port)
                onlineUsers = [i for i in onlineUsers if i[0] != self.sock]
                #print 'QQ  '
                #print  onlineUsers
                #self.sock.close()
                break;
            except:
                print 'other failed'
                break;
            
            
            if data[0]=='exit()' and len(data) == 1:
                #print 'test  ' + data[0] + str(len(data))
                #print '[logout] %s from %s:%s' % (self.name,self.ip,self.port)
                #print onlineUsers
                onlineUsers = [i for i in onlineUsers if i[0] != self.sock]
                #print onlineUsers
                #self.sock.close()
                
                break
            
            
            elif data[0]=='list' and len(data)==1:
                self.sock.send('list ')
                for (sock,name) in onlineUsers:
                    self.sock.send(name+' ')
                self.sock.send('%%%end%%%')
            
           
            elif data[0]=='chat' and len(data)==3:
                users = [i for i in onlineUsers if i[1] == data[1]]
                for (sock,name) in users:
                    sock.send('chat '+self.name+' '+data[2])


            elif data[0]=='sendfile':
                users = [i for i in onlineUsers if i[1] == data[1]]
                sendFile = originData.replace('sendfile ','')
                sendFile = sendFile.replace(data[1]+' ','')
                sendFile = sendFile.replace(data[2]+' ','')
                recvData = data
                while sendFile.find( ' %%%end%%%' )==-1:
                    sendFile += self.sock.recv(BUFFER_SIZE)
                    print 'sendFile '+sendFile
                sendFile = sendFile.replace(' %%%end%%%','')
                for (sock,name) in users:
                    sock.send('sendfile '+self.name+' '+data[2]+' ')
                    sock.send(sendFile)
                    sock.send(' %%%end%%%')

            elif data[0]=='kick' and len(data)==2:
                users = [i for i in onlineUsers if i[1] == data[1]]
                onlineUsers = [i for i in onlineUsers if i[1] != data[1]]
                for (sock,name) in users:
                    sock.send('kick '+self.name)
                    sock.close()
            else:
                print data
        print '[logout] %s from %s:%s' % (self.name,self.ip,self.port)
        self.sock.close()
        # filename='myText.txt'
        # f = open(filename,'rb')
        # while True:
            # l = f.read(BUFFER_SIZE)
            # while (l):
                # self.sock.send(l)
                #print('Sent ',repr(l))
                # l = f.read(BUFFER_SIZE)
            # if not l:
                # f.close()
                # self.sock.close()
                # break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(20)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    name = conn.recv(BUFFER_SIZE)
    newthread = ClientThread(ip,port,conn,name)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
