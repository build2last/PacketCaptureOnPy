# coding:utf-8
import socket

#create an INET, STREAMing socket
s = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
MSGLEN = 20

class mysocket:
	'''demonstration class only
	- coded for clarity, not efficiency
	'''
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(
					socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
			
	def connect(self, host, port):
		self.sock.connect((host, port))
		
	def mysend(self, msg):
		totalsent = 0
		while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent
			
	def myreceive(self):
		chunks = []
		bytes_recd = 0
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return ''.join(chunks)

if __name__ == "__main__":
	HOST = socket.gethostname()    # The remote host
	PORT = 80             # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall('Hello, world')
	data = s.recv(1024)
	s.close()
	print 'Received', repr(data)