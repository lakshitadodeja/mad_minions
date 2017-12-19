import sys,math,random,time,pygame,socket,json
from pygame.locals import *

def main():
    s = socket.socket() 
    host = socket.gethostname() 
    port = 12345        
    s.bind((host, port))
    #s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
    s.listen(5)
    c1, addr1 = s.accept()   
    print 'Got connection from', addr1
    c2, addr2 = s.accept()
    print 'Got connection from', addr2
    val=True
    val2=True
    while True:
        if val:
            i=0
            for i in range(10):
                x=random.randint(0,1200)
                y=random.randint(0,800)
                c1.send(str(x))
                c1.recv(1024)
                c1.send(str(y))
                c1.recv(1024)
                c2.send(str(x))
                c2.recv(1024)
                c2.send(str(y))
                c2.recv(1024)
            val=False
        if val2:
            i=0
            for i in range(20):
                x=random.randint(0,1200)
                y=random.randint(0,800)
                c1.send(str(x))
                c1.recv(1024)
                c1.send(str(y))
                c1.recv(1024)
                c2.send(str(x))
                c2.recv(1024)
                c2.send(str(y))
                c2.recv(1024)
            val2=False
        score1= c1.recv(1024)
        #print score1
        score2= c2.recv(1024)
        #print score2            
        c2.send(score1)
        c1.send(score2)
    s.close

if __name__ == '__main__':
    main()
