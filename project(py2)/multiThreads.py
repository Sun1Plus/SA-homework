#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import with_statement # Required in 2.5
import socket, sys
from contextlib import contextmanager
import threading
import thread
import time



host = ''
port = 51423

Id_Key = {"admin": "admin", "Tang": "001", "Wang": "002", "Li": "003", "Sun": "004"}
Online_Id_IP = {}
Applying_Id_IP = {}

# 准备一个socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置socket选项，SO_REUSEADDR是为了结束后立刻释放此端口，方便调试
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定socket，host为绑定ip地址，为空表示可以绑定到所有接口和地址，port为绑定的端口号
s.bind((host, port))


def tcplink(sock, addr):
    sock.send("Welcome!")
    # data = sock.recv(1024)
    # print data


s.listen(5)
print "Waiting for connections..."
socketlist = []
threads = []


def Serverlisten(thread_name):
    i = 1
    while(i):
        time.sleep(1)
        print thread_name
        sock, addr = s.accept()

        print "i'm running."
        t = threading.Thread(target=tcplink, args=(sock, addr))
        threads.append(t)
        t.start()
        Id = sock.recv(1024)
        sock.send("ID_over")
        Key = sock.recv(1024)
        if (Id_Key.get(Id) == Key):
            Online_Id_IP[Id] = sock
            sock.send("login")


def Serverheart(thread_name):
    i = 1
    while(i):
        i = i+1
        time.sleep(1)

        for Id, socketitem in Online_Id_IP.items():
            print Id, socketitem
            print " Send alive."
            socketitem.send('alive?')
            data = socketitem.recv(1024)
            print data
            if data != "yes":
                del Online_Id_IP[Id]


# 创建两个线程
try:
    thread.start_new_thread(Serverlisten, ("Thread-1",))
    thread.start_new_thread(Serverheart, ("Thread-2",))
except:
    print "Error: unable to start thread"


while 1:
    pass
