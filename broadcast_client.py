import socket
import time
import threading
from threading import Thread
class udpclient():
	def __init__(self):
		self.AMOUNT_BYTES = 1024

		self.BROADCAST_PORT_SEND = 9000
		BROADCAST_PORT_RECV = 9001
		BROADCAST_LISTEN = ''
		self.BROADCAST_SEND = '<broadcast>'

		#SOCKET TO RECEIVE MSG
		self.bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.bsock.bind((BROADCAST_LISTEN,BROADCAST_PORT_RECV))
		self.teste = 0
		
	def loop(self):
		t1 = threading.Thread(target=self.send)
		t1.start()
		while True :
			message , address = self.bsock.recvfrom(self.AMOUNT_BYTES)
			if message == b'ACK':
				self.teste = 1
				return address[0]
	def send(self):
		while self.teste == 0:
			self.bsock.sendto(b"DISCOVER", (self.BROADCAST_SEND, self.BROADCAST_PORT_SEND))
			time.sleep(5)