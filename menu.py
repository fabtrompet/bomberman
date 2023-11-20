import threading
from tkinter import *
import os
from broadcast_client import *
from tcp_server_local import *
from tcp_client import *
from teste import Bomberman
class Carregamento(Frame):
	def __init__(self, parent, op, nick):
		Frame.__init__(self,parent)
		self.pack(fill=BOTH)
		root.protocol("WM_DELETE_WINDOW", self.close)
		self.num = 0
		self.op = op
		self.nick=nick
		self.tela()
		self.create_widgets()
		
	def create_widgets(self):
		self.label = Label(self, bd=0)
		self.label.pack()
		Thread(target=self.animate).start()
		Thread(target=self.conexao).start()

	def tela(self):
		self.texto = Label(self,text="Encontrando Jogador!")
		self.texto.pack()
	def animate(self):
		while True:
			try:
				time.sleep(0.04)
				img = PhotoImage(file="/usr/bin/radio.gif", format="gif - {}".format(self.num))
				self.label.config(image=img)
				self.label.image=img
			
				self.num += 1
			except:
				self.num = 0
	def conexao(self):
		if self.op == 1:
			self.cli = cliente('54.207.57.244')
			self.cli.enviar("entrei")
			resposta = self.cli.receber()
			if resposta == "True":
				self.destroy()
				self.cli.enviar("sorteio")
				resposta = self.cli.receber()
				app = Bomberman(root,resposta,self.cli,self.nick)
				#t1 = threading.Thread(target=app.conexao, args=[self.cli])
				#t1.start()
				app.master.title("Bomberman")
				app.master.geometry("480x480+600+100")
				app.master.resizable(width=False, height=False)
		else:
			udp = udpclient()
			ip = udp.loop()
			self.cli = cliente(ip)
			self.cli.enviar("entrei")
			resposta = self.cli.receber()
			resposta = resposta.decode('utf-8')
			print(resposta)
			if resposta == "True":
				print(resposta)
				self.destroy()
				self.cli.enviar("sorteio")
				resposta = self.cli.receber()
				resposta = resposta.decode('utf-8')
				print(resposta)
				app = Bomberman(root,resposta,self.cli,self.nick)
				#t1 = threading.Thread(target=app.conexao, args=[self.cli])
				#t1.start()
				app.master.title("Bomberman")
				app.master.geometry("1480x1480+1600+1100")
				app.master.resizable(True, True)
	def close(self):
		os._exit(0)

class Menu(Frame):
	def __init__(self, parent):
		Frame.__init__(self,parent)
		self.pack(fill=BOTH, expand=1)
		root.protocol("WM_DELETE_WINDOW", self.close)
		self.tela()
	def tela(self):
		
		self.v = IntVar()
		self.servidorexterno = Radiobutton(self, text="Conectar ao Servidor Externo",variable=self.v, value=1)
		self.servidorexterno.place(x=10,y=50)
		self.servidorlocal = Radiobutton(self, text="Conectar a algum Servidor Local",variable=self.v, value=2)
		self.servidorlocal.place(x=10,y=70)
		self.servidor1 = Radiobutton(self, text="Ser o Servidor",variable=self.v, value=3)
		self.servidor1.place(x=10,y=90)

		self.Button1=Button(self.master, text="Selecione", command=self.seleciona2)
		self.Button1.place(x=20,y=110)

	def seleciona2(self):
		if self.v.get() == 1:
			self.textexterno = Label(self, text="Nick:")
			self.textexterno.place(x=250,y=50)
			self.nickexterno = Entry(self, width="10")
			self.nickexterno.place(x=290,y=50)
			self.servidorexterno['state'] = 'disabled'
			self.servidorlocal['state'] = 'disabled'
			self.servidor1['state'] = 'disabled'
			self.Button1.destroy()
			self.Button1=Button(self.master, text="Selecione seu nick", command=self.seleciona)
			self.Button1.place(x=20,y=110)
		elif self.v.get() == 2:
			self.textexterno = Label(self, text="Nick:")
			self.textexterno.place(x=250,y=50)
			self.nickexterno = Entry(self, width="10")
			self.nickexterno.place(x=290,y=50)
			self.servidorexterno['state'] = 'disabled'
			self.servidorlocal['state'] = 'disabled'
			self.servidor1['state'] = 'disabled'
			self.Button1.destroy()
			self.Button1=Button(self.master, text="Selecione seu nick", command=self.seleciona)
			self.Button1.place(x=20,y=110)
		elif self.v.get() == 3:
			t1 = threading.Thread(target=self.servidor2)
			t1.start()
			self.Button1['state'] = 'disabled'
			self.servidorexterno['state'] = 'disabled'
			self.servidorlocal['state'] = 'disabled'
			self.servidor1['state'] = 'disabled'
			self.texto = Label(self,text="Servidor On!")
			self.texto.pack()
	def seleciona(self):
		if self.v.get() == 1:
			nick = self.nickexterno.get()
			self.destroy()
			app = Carregamento(root,self.v.get(),nick)
			app.master.title("Bomberman")
			app.master.geometry("450x240+600+100")
		elif self.v.get() == 2:
			nick = self.nickexterno.get()
			self.destroy()
			app = Carregamento(root,self.v.get(),nick)
			app.master.title("Bomberman")
			app.master.geometry("450x240+600+100")
	def servidor2(self):
		servidor()
	def close(self):
		os._exit(0)

root = Tk()
app = Menu(root)
app.master.title("Menu")
app.master.geometry("450x240+600+100")
app.master.resizable(True, True)
root.mainloop()