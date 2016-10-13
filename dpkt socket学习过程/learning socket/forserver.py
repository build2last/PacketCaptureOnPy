# coding:utf-8
import socket
import threading
from time import ctime,sleep

def music(func):
        print "client socket: %s. %s" %(func,ctime())
        sleep(1)

#create an INET, STREAMing socket
serversocket = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
"""
A couple things to notice: we used socket.gethostname() so that the socket would be visible to the outside
world. If we had used s.bind((’localhost’, 80)) or s.bind((’127.0.0.1’, 80)) we would still
have a “server” socket, but one that was only visible within the same machine. s.bind((’’, 80)) specifies that
the socket is reachable by any address the machine happens to have.
"""
serversocket.bind((socket.gethostname(), 80))
#become a server socket
serversocket.listen(5)
# 允许至多5个连接在队列中
#   Finally, the argument to listen tells the socket library that we want it to queue up as many as 5 connect requests
#(the normal max) before refusing outside connections.
while 1:
	while 1:
		#accept connections from outside
		(clientsocket, address) = serversocket.accept()
		#now do something with the clientsocket
		#in this case, we'll pretend this is a threaded server
		data = clientsocket.recv(1024)
		if not data: break
		clientsocket.sendall(data)
		ct = threading.Thread(target=music, args=(clientsocket,))
		ct.run()


