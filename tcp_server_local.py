import threading
from random import randint
from broadcast_server import *
from socket import *
import time
import getpass
class servidor(): 
    def __init__(self):
        self.serverPort = 12000
        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.serverSocket.bind(('',self.serverPort))
        self.serverSocket.listen(1)
        self.numeros = []
        self.numeros2 = []
        self.usuarios = []    
        self.loop()

    def tudocerto(self):
        if ((len(self.usuarios)) % 2 == 0):
            self.usuarios[len(self.usuarios)-1].send("True".encode('utf-8'))
            self.usuarios[len(self.usuarios)-2].send("True".encode('utf-8'))
    def play(self, conect):
        self.numeros = []
        numeros2 = self.sortea()
        print(self.usuarios)
        num = self.usuarios.index(conect)
        print(num, numeros2)
        if ((num+1) % 2) == 0:
            self.usuarios[num-1].send(numeros2.encode('utf-8'))
            self.usuarios[num].send(numeros2.encode('utf-8'))
    def quemjoga(self, conect):
        num = self.usuarios.index(conect)
        if (num % 2) == 0:
            self.usuarios[num+1].send("segundo".encode('utf-8'))
            self.usuarios[num].send("primeiro".encode('utf-8'))
    def sortea(self):
        string = ""
        especialbomba=randint(0,133)
        for i in range(0,133):
            if especialbomba == i:
                self.numeros.append(9)
            else: 
                self.numeros.append(randint(0,1))
        for i in self.numeros:
            string = string+"/"+str(i)
        return string


    def receber(self,connectionSocket, addr):
        while 1:
            sentence = connectionSocket.recv(1024)
            sentence = sentence.decode('utf-8')
            print(sentence)
            if sentence == "quemjoga":
                time.sleep(randint(1,5))
                self.quemjoga(connectionSocket)
            elif sentence == "jogar":
                num = self.usuarios.index(connectionSocket)
                if (num % 2) == 0:
                    self.usuarios[num+1].send("true".encode('utf-8'))
                else:
                    self.usuarios[num-1].send("true".encode('utf-8'))
            elif sentence == "entrei":
                self.usuarios.append(connectionSocket)
                self.tudocerto()
            elif sentence == "sorteio":
                self.play(connectionSocket)
            elif sentence == "":
                try:
                    num = self.usuarios.index(connectionSocket)
                    if (num % 2) == 0:
                        try:
                            self.usuarios[num+1].send("desconectado".encode('utf-8'))
                            self.usuarios[num+1].close()
                            self.usuarios.remove(self.usuarios[num+1])
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            
                        except Exception as e:
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            
                        
                    else:
                        try:
                            self.usuarios[num-1].send("desconectado".encode('utf-8'))
                            self.usuarios[num-1].close()
                            self.usuarios.remove(self.usuarios[num-1])
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            
                        except Exception as e:
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            
                except Exception as e:
                    raise e
            elif sentence[:4] == "nick":
                user=getpass.getuser()
                try:
                    arq = open("/home/"+user+"/.ranking.txt", "r")
                    texto = arq.readlines()
                    arq.close()
                except:
                    texto="nick=Nick;tempo=Menor Tempo\n"
                    arq = open("/home/"+user+"/.ranking.txt", "w")
                    arq.write(texto)
                    arq.close()
                    arq = open("/home/"+user+"/.ranking.txt", "r")
                    texto = arq.readlines()
                    arq.close()
                    pass
                teste=True
                for i in range(len(texto)):
                    if texto[i].split(";")[0].split("=")[1] == sentence.split(";")[0].split("=")[1]:
                        if texto[i].split(";")[1].split("=")[1] < sentence.split(";")[1].split("=")[1]:
                            teste=False
                        else:
                            texto.remove(texto[i])
                            teste=True
                if teste:
                    arq = open("/home/"+user+"/.ranking.txt", "w")
                    texto.append(sentence+"\n")
                    for i in texto:
                        arq.write(i)
                    arq.close()
            elif sentence == "acabou":
                user=getpass.getuser()
                arq = open("/home/"+user+"/.ranking.txt", "r")
                texto = arq.read()
                num = self.usuarios.index(connectionSocket)
                if (num % 2) == 0:
                    self.usuarios[num+1].send(texto)
                    self.usuarios[num].send(texto)
                else:
                    self.usuarios[num-1].send(texto)
                    self.usuarios[num].send(texto)
                arq.close()
            else:
                num = self.usuarios.index(connectionSocket)
                if len(sentence) > 3:
                    for i in range(0,len(sentence),3):
                        texto=sentence[i:i+3]
                        if (num % 2) == 0:
                            self.usuarios[num+1].send(texto)
                        else:
                            self.usuarios[num-1].send(texto)
                else:
                    if (num % 2) == 0:
                        self.usuarios[num+1].send(sentence)
                    else:
                        self.usuarios[num-1].send(sentence)

        connectionSocket.close()
        #
    def udpserver(self, nada):
        udpserver()
    def loop(self):
        while 1:
            try:
                threading.Thread(target=self.udpserver, args=(tuple([""]))).start()
                connectionSocket, addr = self.serverSocket.accept()
                threading.Thread(target=self.receber, args=(tuple([connectionSocket, addr]))).start()
            except Exception as e:
                print(e)
                break
                #
                self.serverSocket.close()

