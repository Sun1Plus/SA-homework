import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 51423))



data = s.recv(1024)
print(data)

# send the ID and key
str_Id = "admin"
s.send(str_Id.encode('utf-8'))
s.recv(1024)
str_key = "admin"
s.send(str_key.encode('utf-8'))


if ((s.recv(1024)).decode() == "login"):
    myname = socket.getfqdn(socket.gethostname())
    print(myname)
    myaddr = socket.gethostbyname(myname)
    print(myaddr)

    while 1:
        data = s.recv(1024).decode()
        time.sleep(1)
        print(data)
        print(data=='alive?')
        if data =='alive?':
            str_yes = "yes"
            s.send(str_yes.encode('utf-8'))
        else:
            break