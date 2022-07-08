""""
AUTORES:	
		Mary Anne Calle Davies
		Victor Hugo Hinojosa Pinto
		Manuel Rodrigo Ramos Sánchez
		Adriana Raquel Linares Garrafa
		Gustavo Alonso Liñán Salinas
"""

#Librerías a importar
import random
import pygame
from pygame.locals import *

#Importamos Clases y Métodos del archivo frogger.py
from frogger import *

#Actores en el videojuego

#Clase Rectángulo (forma de todos los objetos)
class Rectangle:

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def intersects(self, other):
		left = self.x
		top = self.y
		right = self.x + self.w
		bottom = self.y + self.h

		oleft = other.x
		otop = other.y
		oright = other.x + other.w
		obottom = other.y + other.h

		return not (left >= oright or right <= oleft or top >= obottom or bottom <= otop)

#Clase Lane (Carriles de fondo)
class Lane(Rectangle):

	def __init__(self, y, c=None, n=0, l=0, spc=0, spd=0):
		super(Lane, self).__init__(0, y * g_vars['grid'], g_vars['width'], g_vars['grid'])
		self.type = t
		self.color = c
		self.obstacles = []
		offset = random.uniform(0, 200)
		if self.type == 'car':
			o_color = (128, 128, 128)
		if self.type == 'log':
			o_color = (185, 122, 87)
		for i in range(n):
			self.obstacles.append(Obstacle(offset + spc * i, 
				y * g_vars['grid'], l * g_vars['grid'], g_vars['grid'], spd, o_color))

#Clase Frog (sapo que controla el jugador)
class Frog(Rectangle):

	def __init__(self, x, y, w):
		super(Frog, self).__init__(x, y, w, w)
		self.x0 = x
		self.y0 = y
		self.color = (34, 177, 76)
		self.attached = None

	def reset(self):
		self.x = self.x0
		self.y = self.y0
		self.attach(None)

	def move(self, xdir, ydir):
		self.x += xdir * g_vars['grid']
		self.y += ydir * g_vars['grid']

	def attach(self, obstacle):	
		self.attached = obstacle

	def update(self):
		if self.attached is not None:
			self.x += self.attached.speed

		if self.x + self.w > g_vars['width']:
			self.x = g_vars['width'] - self.w
		
		if self.x < 0:
			self.x = 0
		if self.y + self.h > g_vars['width']:
			self.y = g_vars['width'] - self.w
		if self.y < 0:
			self.y = 0

	def draw(self):
		rect = Rect( [self.x, self.y], [self.w, self.h] )
		pygame.draw.rect( g_vars['window'], self.color, rect )

#Clase Obstacle (Obstáculos que esquiva el jugador para ganar o que colisiona para perder)
class Obstacle(Rectangle):

	def __init__(self, x, y, w, h, s, c):
		super(Obstacle, self).__init__(x, y, w, h)
		self.color = c
		self.speed = s

	def update(self):
		self.x += self.speed
		if self.speed > 0 and self.x > g_vars['width'] + g_vars['grid']:
			self.x = -self.w
		elif self.speed < 0 and self.x < -self.w:
			self.x = g_vars['width']

	def draw(self):
		pygame.draw.rect( g_vars['window'], self.color, Rect( [self.x, self.y], [self.w, self.h] ) )

