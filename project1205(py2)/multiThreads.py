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

Id_Key = {"admin": "admin", "flask": "flask", "Tang": "001", "Wang": "002", "Li": "003", "Sun": "004"}
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


s.listen(100)
print "Waiting for connections..."
socketlist = []
threads = []


# flask
def flask_link(thread_name):
    sockflask, addrflask = s.accept()
    t = threading.Thread(target=tcplink, args=(sockflask, addrflask))
    threads.append(t)
    t.start()

    Id = sockflask.recv(1024)
    sockflask.send("ID_over")
    Key = sockflask.recv(1024)

    while(1):
        print thread_name

        option = sockflask.recv(1024)
        if(option == "permit"):
            permit_Id = sockflask.recv(1024)
            permit_option = sockflask.recv(1024)

            Serverpermit(permit_Id, permit_option)
        elif(option == "close"):
            close_Id = sockflask.recv(1024)
            socket_close(close_Id)





def Serverlisten(thread_name):
    while(1):
        time.sleep(0.5)
        print thread_name
        sock, addr = s.accept()

        print "i'm runing"
        t = threading.Thread(target=tcplink, args=(sock, addr))
        threads.append(t)
        t.start()
        # Id = sock.recv(1024)
        Id = sock.recv(1024)
        sock.send("ID_over")
        Key = sock.recv(1024)
        if (Id_Key.get(Id) == Key):
            Applying_Id_IP[Id] = sock


# # 想办法让他得到一个permit_socket
# def Serverpermit(thread_name):
#     while(1):
#         print thread_name
#
#         # 在这里传过来
#         permit_socket =
#
#         for Id, socketitem in Applying_Id_IP.items():
#             if socketitem == permit_socket:
#                 socketitem.send("login")
#                 Online_Id_IP[Id] = socketitem
#                 del Applying_Id_IP[Id]


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

            # record the time and Online size
            localtime = time.asctime(time.localtime(time.time()))
            online_num = len(Online_Id_IP)


# 想办法让他得到一个permit_socket
def Serverpermit(per_Id, per_option):
    for Id, socketitem in Applying_Id_IP.items():
        if per_Id == Id:
            if(per_option == "Yes"):
                socketitem.send("login")
                Online_Id_IP[Id] = socketitem
            else:
                socketitem.close()
            del Applying_Id_IP[Id]


def socket_close(Id_close):
    for Id, socketitem in Online_Id_IP.items():
        if(Id_close == Id):
            socketitem.close()
            del Online_Id_IP[Id]


# 创建两个线程
try:
    thread.start_new_thread(flask_link, ("Thread-0",))
    thread.start_new_thread(Serverlisten, ("Thread-1",))
    thread.start_new_thread(Serverheart, ("Thread-2",))
except:
    print "Error: unable to start thread"


while 1:
    pass
