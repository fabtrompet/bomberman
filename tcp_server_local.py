import thread
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
            self.usuarios[len(self.usuarios)-1].send("True")
            self.usuarios[len(self.usuarios)-2].send("True")
    def play(self, conect):
        self.numeros = []
        numeros2 = self.sortea()
        num = self.usuarios.index(conect)
        if (num % 2) == 0:
            self.usuarios[num+1].send(numeros2)
            self.usuarios[num].send(numeros2)
    def quemjoga(self, conect):
        num = self.usuarios.index(conect)
        if (num % 2) == 0:
            self.usuarios[num+1].send("segundo")
            self.usuarios[num].send("primeiro")
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
            #print sentence
            if sentence == "quemjoga":
                time.sleep(randint(1,5))
                self.quemjoga(connectionSocket)
            elif sentence == "jogar":
                num = self.usuarios.index(connectionSocket)
                if (num % 2) == 0:
                    self.usuarios[num+1].send("true")
                else:
                    self.usuarios[num-1].send("true")
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
                            self.usuarios[num+1].send("desconectado")
                            self.usuarios[num+1].close()
                            self.usuarios.remove(self.usuarios[num+1])
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            thread.exit()
                        except Exception as e:
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            thread.exit()
                        
                    else:
                        try:
                            self.usuarios[num-1].send("desconectado")
                            self.usuarios[num-1].close()
                            self.usuarios.remove(self.usuarios[num-1])
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            thread.exit()
                        except Exception as e:
                            self.usuarios.remove(connectionSocket)
                            connectionSocket.close()
                            thread.exit()
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
        thread.exit()
    def udpserver(self, nada):
        udpserver()
    def loop(self):
        while 1:
            try:
                thread.start_new_thread(self.udpserver, tuple([""]))
                connectionSocket, addr = self.serverSocket.accept()
                thread.start_new_thread(self.receber, tuple([connectionSocket, addr]))
            except:
                thread.exit()
                self.serverSocket.close()

