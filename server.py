import socket
import time
from threading import Thread
from SocketServer import ThreadingMixIn


TCP_IP = '188.166.241.205'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock,name):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.name = name
        print "[login] "+name+" from "+ip+":"+str(port)

    def run(self):
        while True:
            try:
                data = self.sock.recv(BUFFER_SIZE)
                data = data.split()
                if data[0]=='exit()' and len(data) == 1:
                    print '%s from %s:%s connection closed' % (self.name,self.ip,self.port)
                    self.sock.close()
                    break
                else:
                    print data
            except IndexError:
                print '%s from %s:%s connection closed' % (self.name,self.ip,self.port)
                break;
            except:
                print 'other failed'
                break;
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
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    name = conn.recv(BUFFER_SIZE)
    newthread = ClientThread(ip,port,conn,name)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
