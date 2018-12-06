import socket
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 51423))


data = s.recv(1024)
print data

# send the ID and key
s.send("admin")
s.recv(1024)
s.send("admin")


if (s.recv(1024) == "login"):
    myname = socket.getfqdn(socket.gethostname(  ))
    print myname
    myaddr = socket.gethostbyname(myname)
    print myaddr

    while 1:
        data = s.recv(1024)
        time.sleep(1)
        print data
        print data=='alive?'
        if data =='alive?':
            s.send("yes")
        else:
            break;