#_*_ coding:utf-8 _*_
from __future__ import with_statement # Required in 2.5
import socket, sys
import time,threading
import os, time
from contextlib import contextmanager


host = ''
port = 51423

#准备一个socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#设置socket选项，SO_REUSEADDR是为了结束后立刻释放此端口，方便调试
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#绑定socket，host为绑定ip地址，为空表示可以绑定到所有接口和地址，port为绑定的端口号
s.bind((host,port))


#指明在处理链接时，允许有多少个未决连接在队列中等待
s.listen(5)
print "Waiting for connections..."

socketlist = []
threads = []

def tcplink(sock, addr):
    sock.send("Welcome!")
    data = sock.recv(1024)
    print data



i=1
while (i):
    try:
        with time_limit(1):
            if(i%20==0):
                sock, addr = s.accept()
                socketlist.append(sock)
                print "i'm running."
                t = threading.Thread(target=tcplink, args=(sock,addr))
                threads.append(t)
                t.start()
    except TimeoutException, msg:
        print ""

    i = i+1

    if(i%200==0):
        print "begin send heart beat"
        for socketitem in socketlist:
            print socketitem
            print " send alive"
            socketitem.send('alive?')
            data = socketitem.recv(1024)
            print data
            if data != "yes":
                socketlist.remove(socketitem)
        print "show socket list:"
        print socketlist

    if(i%1200 == 0):
        print '--------------------------------------------------'
        print 'delete the second one:'
        socketlist[1].close()
        socketlist.remove(socketlist[1])
        print '--------------------------------------------------'



