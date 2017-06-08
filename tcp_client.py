from socket import *

class cliente():
    def __init__(self, ip):
        self.serverName = ip
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName,self.serverPort))
    def enviar(self, string):
        self.clientSocket.send(string)
    def receber(self):
        resposta = self.clientSocket.recv(1024)
        return resposta
