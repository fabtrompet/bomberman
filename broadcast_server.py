# -*- coding: utf-8 -*-
import socket
class udpserver():
	def __init__(self):
		AMOUNT_BYTES = 1024

		BROADCAST_PORT_SEND = 9001      # Porta que o cliente estará escutando
		BROADCAST_PORT_RECV = 9000      # Porta que o cliente irá enviar mensagem
		BROADCAST_LISTEN = ''           # Interface que será utilizada, se você pôr 127.255.255.255, ele só responderá a chamadas locais

		bsock = socket.socket(socket.AF_INET,      #Internet Address Family IPv4
		                      socket.SOCK_DGRAM)   #UDP Protocol
		bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		bsock.bind((BROADCAST_LISTEN, BROADCAST_PORT_RECV))

		while True :
		    message , address = bsock.recvfrom(AMOUNT_BYTES)
		    print("message '{0}' from : {1}".format(message, address))
		    if message == b'DISCOVER':
		        bsock.sendto(b"ACK", (address[0] ,BROADCAST_PORT_SEND))
