import socket
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 51423))



data = s.recv(1024)
print data

# send the ID and key
s.send("flask")
s.recv(1024)
s.send("flask")

s.send("permit")
s.send("admin")
s.send("Yes")

s.send("permit")
s.send("Wang")
s.send("Yes")

s.send("close")
s.send("admin")
s.send("No")