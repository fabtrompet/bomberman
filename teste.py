# -*- coding: utf-8 -*-
import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk
import threading
import os
from threading import Thread
import time
from random import randint
class Bomber(Frame):
	def __init__(self, parent,numeros, con):
		Frame.__init__(self, parent)
		self.fogo=[]
		numeros = numeros.split("/")
		self.cli=con
		self.sou=0
		rows=15
		columns=15
		#Frame.__init__(self,parent)
		cont=1
		self.blocos=[]
		self._widgets = []
		for row in range(rows):
			current_row = []
			for column in range(columns):
				label = Label(self)
				if row == 0 or row  == 14:
					label.configure(bg="gray")
					label.grid(row=row, column=column, sticky="nsew")
				elif column == 0 or column == 14:
					label.configure(bg="gray")
					label.grid(row=row, column=column, sticky="nsew")
				else:
					if row % 2 == 0 and column % 2 == 0:
						label.configure(bg="gray")
						label.grid(row=row, column=column, sticky="nsew")
					else:
						true = int(numeros[cont])
						if row == 1 and column == 1:
							true = 1
						if row == 2 and column == 1:
							true = 1
						if row == 1 and column == 2:
							true = 1
						if row == 13 and column == 13:
							true = 1
						if row == 12 and column == 13:
							true = 1
						if row == 13 and column == 12:
							true = 1
						if true == 0:
							self.blocos.append((column,row))
							label.configure(bg="blue")
							label.grid(row=row, column=column, sticky="nsew")
						elif true == 9:
							self.blocos.append((column,row))
							label.configure(bg="white")
							label.grid(row=row, column=column, sticky="nsew")
						else:
							label.configure(bg="green")
							label.grid(row=row, column=column, sticky="nsew")
						cont+=1
				current_row.append(label)
			self._widgets.append(current_row)
		for column in range(columns):
			self.grid_columnconfigure(column, pad=28)
		for row in range(rows):
			self.grid_rowconfigure(row, pad=14)
		self.pack(fill=BOTH, expand=1)
		parent.protocol("WM_DELETE_WINDOW", self.close)
		self.conexao()
		self.tela(parent)
		Thread(target=self.conexao2).start()
	def tela(self,parent):
		#self.img2 = ImageTk.PhotoImage(Image.open('tartaruga.png'))
		#self.img = Label(self, image=self.img2)
		#self.img.image=self.img2
		#self.img.place(x=32,y=32)
		#parent.bind("<Down>",self.baixo)
		#parent.bind("<Up>",self.cima)
		#parent.bind("<Left>",self.esquerda)
		#parent.bind("<Right>",self.direita)
		#parent.bind("<space>",self.bomba)

		self.play1 = player(self,parent, self.sou)
		self.play2 = player(self,parent, self.sou,self.play1)
	def conexao(self):
		self.cli.enviar("quemjoga")
		teste = self.cli.receber()
		self.sou = teste
		#texto = "Você joga por "+teste
		#toplevel = Toplevel()
		#label1 = Label(toplevel, text=texto, height=5, width=30)
		#label1.pack(side="top")
	def conexao2(self):
		while 1:
			resposta = self.cli.receber()
			if resposta == "baixo":
				self.play2.baixo("baixo")
			elif resposta == "cima":
				self.play2.cima("cima")
			elif resposta == "esquerda":
				self.play2.esquerda("esquerda")
			elif resposta == "direita":
				self.play2.direita("direita")
			elif resposta == "bomba":
				self.play2.bomba("bomba")
	def close(self):
		os._exit(0)


class player():
	def __init__(self,teste,parent,play,check=None):
		self.testabomba=1
		self.master = teste
		self.outro = check
		self.play = play
		if play == "primeiro":
			if check == None:
				self.img2 = ImageTk.PhotoImage(Image.open("play13.gif"))
				self.img = Label(self.master, bg="green",image=self.img2)
				self.img.image=self.img2
				self.img.place(x=32,y=32)
			else:
				self.img2 = ImageTk.PhotoImage(Image.open('play23.gif'))
				self.img = Label(self.master, bg="green",image=self.img2)
				self.img.image=self.img2
				self.img.place(x=416,y=416)				
		else:
			if check == None:
				self.img2 = ImageTk.PhotoImage(Image.open('play23.gif'))
				self.img = Label(self.master, bg="green",image=self.img2)
				self.img.image=self.img2
				self.img.place(x=416,y=416)
			else:
				self.img2 = ImageTk.PhotoImage(Image.open('play13.gif'))
				self.img = Label(self.master, bg="green", image=self.img2)
				self.img.image=self.img2
				self.img.place(x=32,y=32)
		if check == None:
			parent.bind("<Down>",self.baixo)
			parent.bind("<Up>",self.cima)
			parent.bind("<Left>",self.esquerda)
			parent.bind("<Right>",self.direita)
			parent.bind("<space>",self.bomba)
	def baixo(self,event):
		testando = self.checaposicao(self.img.winfo_x(),self.img.winfo_y()+32,"x")
		print testando 
		if testando == True:
			if event != "baixo":
				self.master.cli.enviar("baixo")
			self.lastx=self.img.winfo_x()
			self.lasty=self.img.winfo_y()+32
			if self.play == "primeiro":
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play13.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play23.gif'))
			else:
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play23.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play13.gif'))
			self.img.configure(image=img2)
			self.img.image = img2
			self.img.place(x=self.img.winfo_x(),y=self.img.winfo_y()+32)
		elif testando == "morreu1" or testando == "morreu2":
			self.morreu(testando)
			if event != "baixo":
				self.master.cli.enviar("baixo")
			self.lastx=self.img.winfo_x()
			self.lasty=self.img.winfo_y()+32
			if self.play == "primeiro":
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play13.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play23.gif'))
			else:
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play23.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play13.gif'))
			self.img.configure(image=img2)
			self.img.image = img2
			self.img.place(x=self.img.winfo_x(),y=self.img.winfo_y()+32)
			
		self.master.update()
	def morreu(self,teste):
		print "aosfuhaisufhaisufhaiosufhio"
		if teste == "morreu1":
			texto = "Você morreu Perdeu"
			toplevel = Toplevel()
			label1 = Label(toplevel, text=texto, height=5, width=30)
			label1.pack(side="top")
		elif teste == "morreu2":
			texto = "Você morreu Perdeu"
			toplevel = Toplevel()
			label1 = Label(toplevel, text=texto, height=5, width=30)
			label1.pack(side="top")

	def cima(self,event):
		if self.checaposicao(self.img.winfo_x(),self.img.winfo_y()-32,"x"):
			if event != "cima":
				self.master.cli.enviar("cima")
			if self.play == "primeiro":
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play11.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play21.gif'))
			else:
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play21.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play11.gif'))
			self.img.configure(image=img2)
			self.img.image = img2
			self.lastx=self.img.winfo_x()
			self.lasty=self.img.winfo_y()-32
			self.img.place(x=self.img.winfo_x(),y=self.img.winfo_y()-32)
		self.master.update()
	def esquerda(self,event):
		if self.checaposicao(self.img.winfo_x()-32,self.img.winfo_y(),"y"):
			if event != "esquerda":
				self.master.cli.enviar("esquerda")
			if self.play == "primeiro":
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play14.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play24.gif'))
			else:
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play24.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play14.gif'))
			self.img.configure(image=img2)
			self.img.image = img2
			self.lastx=self.img.winfo_x()-32
			self.lasty=self.img.winfo_y()
			self.img.place(x=self.img.winfo_x()-32,y=self.img.winfo_y())
		self.master.update()
	def direita(self,event):
		if self.checaposicao(self.img.winfo_x()+32,self.img.winfo_y(),"y"):
			if event != "direita":
				self.master.cli.enviar("direita")
			if self.play == "primeiro":
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play12.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play22.gif'))
			else:
				if self.outro == None:
					img2 = ImageTk.PhotoImage(Image.open('play22.gif'))
				else:
					img2 = ImageTk.PhotoImage(Image.open('play12.gif'))
			self.img.configure(image=img2)
			self.img.image = img2
			self.lastx=self.img.winfo_x()+32
			self.lasty=self.img.winfo_y()
			self.img.place(x=self.img.winfo_x()+32,y=self.img.winfo_y())
		self.master.update()
	def bomba(self,event):
		if self.testabomba == 1:
			if event != "bomba":
				self.master.cli.enviar("bomba")
			t1 = Thread(target=self.bomba2)
			t1.start()
	def bomba2(self):
		self.testabomba=0
		self.img2 = ImageTk.PhotoImage(Image.open('bomba.gif'))
		self.img3 = Label(self.master,bg='green',image=self.img2)
		self.img3.image=self.img2
		self.img3.place(x=self.lastx,y=self.lasty)
		lastx = self.lastx
		lasty = self.lasty
		self.master.update()
		teste = lastx / 32
		teste2 = lasty / 32
		self.master.blocos.append((teste,teste2))
		time.sleep(2)
		self.master.fogo.append(self.master._widgets[teste2][teste])
		self.master._widgets[teste2][teste].configure(bg="red")
		veri=True
		if (lastx+32) <= 416:
			for x in range(32,417,64):
				for y in range(64,417,64):
					if lastx == x and lasty == y:
						veri=False
			if veri:
				self.master.fogo.append(self.master._widgets[teste2][teste+1])
				self.master._widgets[teste2][teste+1].configure(bg="red")
		else:
			veri=False		
		veri2=True
		if (lastx-32) >= 32:
			for x in range(32,417,64):
				for y in range(64,417,64):
					if lastx == x and lasty == y:
						veri2=False
			if veri2:
				self.master.fogo.append(self.master._widgets[teste2][teste-1])
				self.master._widgets[teste2][teste-1].configure(bg="red")
		else:
			veri2=False
		veri3=True		
		if (lasty+32) <= 416:
			for x in range(64,417,64):
				for y in range(32,417,64):
					if lastx == x and lasty == y:
						veri3=False
			if veri3:
				self.master.fogo.append(self.master._widgets[teste2+1][teste])
				self.master._widgets[teste2+1][teste].configure(bg="red")
		else:
			veri3=False
		veri4=True
		if (lasty-32) >= 32:
			for x in range(64,417,64):
				for y in range(32,417,64):
					if lastx == x and lasty == y:
						veri4=False
			if veri4:
				self.master.fogo.append(self.master._widgets[teste2-1][teste])
				self.master._widgets[teste2-1][teste].configure(bg="red")
		else:
			veri4=False
		self.img3.destroy()
		self.testabomba=1
		try:
			self.master.blocos.remove((teste,teste2))
			
		except:
			pass
		try:
			self.master.blocos.remove((teste+1,teste2))
		except:
			pass
		try:
			self.master.blocos.remove((teste-1,teste2))
		except:
			pass
		try:
			self.master.blocos.remove((teste,teste2+1))
		except:
			pass
		try:
			self.master.blocos.remove((teste,teste2-1))
		except:
			pass
		try:
			self.master.play1.checaposicao(self.master.play1.lastx,self.master.play1.lasty,"parado")
			self.master.play2.checaposicao(self.master.play2.lastx,self.master.play2.lasty,"parado")
		except:
			pass	
		#self.checaposicao(self.lastx,self.lasty, "parado")	
		time.sleep(1)	
		if veri:
				self.master.fogo.remove(self.master._widgets[teste2][teste+1])
				self.master._widgets[teste2][teste+1].configure(bg="green")
		if veri2:
				self.master.fogo.remove(self.master._widgets[teste2][teste-1])
				self.master._widgets[teste2][teste-1].configure(bg="green")
		if veri3:
				self.master.fogo.remove(self.master._widgets[teste2+1][teste])
				self.master._widgets[teste2+1][teste].configure(bg="green")
		if veri4:
				self.master.fogo.remove(self.master._widgets[teste2-1][teste])
				self.master._widgets[teste2-1][teste].configure(bg="green")
		self.master.fogo.remove(self.master._widgets[teste2][teste])
		self.master._widgets[teste2][teste].configure(bg="green")
		return True
	def checaposicao(self, x, y, caminho):
		#print self.blocos
		#print self.master.sou,x,y, caminho
		if x < 32 or y > 416 or x > 416 or y < 32:
			return False
		elif x >= 32 and y >= 32:
			for xy in self.master.blocos:
				#print x,y
				if x > (xy[0]-1) * 32 and x < (xy[0]+1) * 32 and y > (xy[1]-1)*32 and y < (xy[1]+1)*32:
					return False
			teste,teste2 = self.master.grid_location(x,y)
			if caminho == "x":
				for i in range(32,417,64):
					if x == i:
						if self.master._widgets[teste2+1][teste+1] in self.master.fogo:
							self.img.destroy()
							if self.master.sou == "primeiro":
								return "morreu1"
							else:
								return "morreu2"
							print "pegou fogo"
						return True
			elif caminho == "y":
				for i in range(32,417,64):
					if y == i:
						if self.master._widgets[teste2+1][teste+1] in self.master.fogo:
							self.img.destroy()
							if self.master.sou == "primeiro":
								return "morreu1"
							else:
								return "morreu2"
							print "pegou fogo"
						return True
			elif caminho == "parado":
				print teste2+1,teste+1
				if self.master._widgets[teste2+1][teste+1] in self.master.fogo:
					self.img.destroy()
					if self.master.sou == "primeiro":
						return "morreu1"
					else:
						return "morreu2"
					print "pegou fogo"
		else:
			return True