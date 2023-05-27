import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from random import randint
from math import *
import pygame
import numpy as np
import ctypes
#from _ctypes import FreeLibrary, _SimpleCData
from _ctypes import _SimpleCData
from subprocess import Popen
from sys import platform
from time import sleep, time

class vect :
	def __init__(self, list = []) -> None:
		self.coords = list

	def __add__(self, v) :
		if (l:=len(v)) == len(self) :
			return vect([self.coords[0]+v[0], self.coords[1]+v[1]])

	def __iadd__(self, v):
		if (l:=len(v)) == len(self) :
			for i in range(l) :
				self.coords[i] += v[i]
		return self

	def __len__(self) :
		return len(self.coords)

	def __mul__(self, v) :
		if type(v) == type(self) :
			d = 0
			d = self.coords[0]*v[0]+self.coords[1]*v[1]
			return d
		return vect([ux*v for ux in self.coords])

	def __truediv__(self, v):
		return vect([ux/v for ux in self.coords])

	def __getitem__(self, index):
		return self.coords[index]

	def __setitem__(self, index, value) :
		self.coords.__setitem__(index, value)

	def __append__(self, item) :
		self.coords.append(item)

	def __sub__(self, v) :
		return vect([self.coords[0]-v[0], self.coords[1]-v[1]])

	def __str__(self) :
		return str(self.coords)

	def normalize(self) :
		if (n := norm(self.coords)) :
			self.coords = vect([self.coords[0]/n, self.coords[1]/n])
		return self


def norm(u) :
	n = 0
	for c in u :
		n += c**2
	return sqrt(n)

def mean(l) :
	s = 0
	for e in l :
		s+= e
	return e/len(l)

def angle(u, v) :
	return acos((u*v)/(norm(u)*norm(v)))

def rand() :
	return randint(0,10**10)

class boid :
	boidslist = []
	nextid = 0
	masscenter = vect([0,0])
	rseek = 60
	rfollow = 40
	rflee = 20
	# def __init__(self, position =[0.,0.], velocity=[0.,0.], rseek=60, rfollow=40, rflee=20, color=[255,255,255,255]):
	def __init__(self, position =[0.,0.], velocity=[0.,0.], color=[255,255,255,255]):
	# def __init__(self, position =[0.,0.], velocity=[0.,0.], rseek=60, rfollow=40, rflee=450, color=[255,255,255,255]):
	# def __init__(self, position =[0.,0.], velocity=[0.,0.], rseek=120, rfollow=80, rflee=15, color=[255,255,255,255]):
	# def __init__(self, position =[0.,0.], velocity=[0.,0.], rseek=120, rfollow=70, rflee=15, color=[255,255,255,255]):
		self.id = boid.nextid
		boid.nextid += 1
		self.position = vect(position)
		self.velocity = vect(velocity)
		self.color = color
		boid.boidslist.append(self)

	def move(self) :
		self.position += self.velocity

	def updateVelocity(self, x_pos, y_pos, x_vel, y_vel) :
		vel = self.reaction2(x_pos, y_pos, x_vel, y_vel)
		# if(vel[0] != 0) and self is boid.boidslist[0]: print(self.velocity)
		# if(vel[0] != 0) and self is boid.boidslist[0]: print(self.position)
		self.velocity += (self.getSubMassCenter()-self.position).normalize()*0.1
		# self.velocity += (self.getSubMassCenter()-self.position).normalize()*1
		self.velocity += vel#.normalize()
		# vel_max = 100
		vel_max = 5
		if nv := norm(self.velocity) > vel_max:
			self.velocity.normalize()
			self.velocity *= vel_max
		# if (self.)
		# self.velocity.normalize()
		# self.velocity.normalize()


		for c in [0, 1] :
			if self.position[c] > 1000 :
				self.velocity[c] = -1
			if self.position[c] < 0 :
				self.velocity[c] = 1
			self.position[c] += (self.velocity[c])*1

	def reaction(self, boidslist) :
		vel = vect([0.,0.])
		for b in boid.boidslist :
			v = b.position-self.position
			nv = norm(v)
			if nv < self.rflee :
				vel -= v.normalize()
			elif nv < self.rfollow :
				vel += b.velocity.normalize()*0.2
			elif nv < self.rseek :
				vel += v.normalize()*0.01
		if nv:=norm(vel) > 0 :
			return vel/nv
		return vel

	def reaction2(self, x_pos, y_pos, x_vel, y_vel) :
		# vel = vect([0.,0.])
		# dx = x_pos-self.position[0]
		# dy = y_pos-self.position[1]
		dpos = np.array([x_pos-self.position[0], y_pos-self.position[1]])
		dists = np.sqrt(dpos[0]**2+dpos[1]**2)
		Vels = np.array([x_vel, y_vel])
		nvs = np.sqrt(x_vel**2+y_vel**2)
		vel = vect(list(-1*(dpos[:,ids := np.where((dists < self.rflee) * (dists > 1e-14))[0]] / dists[ids]).sum(1) \
			+ 0.1*(Vels[:,ids := np.where((dists >= self.rflee) * (dists < self.rfollow) * (nvs > 1e-14))[0]] / nvs[ids]).sum(1) \
			+ 0.01*(dpos[:,ids := np.where((dists >= self.rfollow) * (dists < self.rseek) * (dists > 1e-14))[0]] / dists[ids]).sum(1)))
		# for b in boid.boidslist :
		# 	v = b.position-self.position
		# 	nv = norm(v)
		# 	if nv < self.rflee :
		# 		vel -= v.normalize()
		# 	elif nv < self.rfollow :
		# 		vel += b.velocity.normalize()*0.2
		# 	elif nv < self.rseek :
		# 		vel += v.normalize()*0.01
		if nv:=norm(vel) > 0 :
			return vel/nv
		return vel

	def updateGroupMassCenter() :
		g = vect([0,0])
		for b in boid.boidslist :
			g += b.position
		boid.masscenter = g/len(boid.boidslist)

	def getSubMassCenter(self) :
		return vect(boid.masscenter*boid.nextid-self.position)/(boid.nextid-1)

	def draw(self, window) :
#		if self == boid.boidslist[0] :
#			pygame.draw.circle(window, pygame.Color(0,255,255,75), self.position, self.rseek)
#			pygame.draw.circle(window, pygame.Color(255,255,0,75), self.position, self.rfollow)
#			pygame.draw.circle(window, pygame.Color(255,0,0,75), self.position, self.rflee)
		pygame.draw.circle(window, pygame.Color(*(self.color)), self.position, 3)

if __name__ == "__main__" :

	winsize = [1000, 1000]
	# nbboids = 1
	# nbboids = 10
	# nbboids = 125
	# nbboids = 500
	# nbboids = 1000
	# nbboids = 3000
	nbboids = 1000

	# boid([rand()%winsize[0], rand()%winsize[1]], [float(rand()%2),float(rand()%2)], color=(255, 0, 255))
	for i in range(0,nbboids) :
		# boid([rand()%winsize[0], rand()%winsize[1]], [float(rand()%2),float(rand()%2)], color=(0,200,int(i/nbboids*200),255)) #-int(i/nbboids*255)
		# boid([rand()%800+100, rand()%800+100], [float(rand()%2),float(rand()%2)], color=(0,200,int(i/nbboids*200),255)) #-int(i/nbboids*255)
		boid([rand()%800+100, rand()%800+100], [0.01,0.01], color=(0,200,int(i/nbboids*200),255)) #-int(i/nbboids*255)
	# boid([800, 100], [0,0], color=(255, 0, 255))
	# boid([100, 100], [0,0], color=(0,200,int(0/nbboids*200)))

	pygame.init()
	win = pygame.display.set_mode(winsize)
	clock = pygame.time.Clock()
	running = True
	dt = 0

	# sleep(1)
	Arr_t = ctypes.c_double*nbboids
	doubleArr = Arr_t*2
	# Pos = doubleArr(0)
	Pos = doubleArr(Arr_t(*([0]*nbboids)), Arr_t(*([0]*nbboids)))
	Vel = doubleArr(Arr_t(*([0]*nbboids)), Arr_t(*([0]*nbboids)))
	Pos1 = doubleArr(Arr_t(*([0]*nbboids)), Arr_t(*([0]*nbboids)))
	Vel1 = doubleArr(Arr_t(*([0]*nbboids)), Arr_t(*([0]*nbboids)))
	# Vel = doubleArr([Arr_t(np.zeros((nbboids))), Arr_t(np.zeros((nbboids)))])
	# Pos1 = doubleArr([Arr_t(np.zeros((nbboids))), Arr_t(np.zeros((nbboids)))])
	# Vel1 = doubleArr([Arr_t(np.zeros((nbboids))), Arr_t(np.zeros((nbboids)))])

	# print(ctypes.addressof(Pos))
	# print(ctypes.addressof(Pos[0]))
	# print(ctypes.addressof(Pos[1]))
	# print(Pos[0][0])
	# exit()

	# rflee_c = ctypes.c_double(boid.rflee)
	# rfollow_c = ctypes.c_double(boid.rfollow)
	# rseek_c = ctypes.c_double(boid.rseek)
	rflee_c = ctypes.c_double(20)
	rfollow_c = ctypes.c_double(45)
	rseek_c = ctypes.c_double(70)
	N_c = ctypes.c_int(nbboids)
	centerx_c = ctypes.c_double(0)
	centery_c = ctypes.c_double(0)
	vmax_c = ctypes.c_double(20)
	log_slope_c = ctypes.c_double(6)

	for i in range(nbboids):
		Pos[0][i] = boid.boidslist[i].position[0]
		Pos[1][i] = boid.boidslist[i].position[1]
		Vel[0][i] = boid.boidslist[i].velocity[0]
		Vel[1][i] = boid.boidslist[i].velocity[1]

	if platform == "win32": # or platform == "win64" ?
		p = Popen("nmake.exe")
		p.wait()
		dll = ctypes.WinDLL(".\\boid.dll")
	else:
		p = Popen("make")
		p.wait()
		dll = ctypes.CDLL("/home/shyguy/Programmation/Python/Boids/Python/libboid.so")
		# exit()

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				running = False

		win.fill("black")

		boid.updateGroupMassCenter()
		centerx_c.value = boid.masscenter[0]
		centery_c.value = boid.masscenter[1]
		dll.update_velocity(N_c, Pos, Vel, Pos1, Vel1, centerx_c, centery_c,\
		       rflee_c, rfollow_c, rseek_c, vmax_c, log_slope_c)
		# x_pos = np.array([bo.position[0] for bo in boid.boidslist])
		# y_pos = np.array([bo.position[1] for bo in boid.boidslist])
		# x_vel = np.array([bo.velocity[0] for bo in boid.boidslist])
		# y_vel = np.array([bo.velocity[1] for bo in boid.boidslist])
		for i in range(nbboids):
			boid.boidslist[i].position[0] = Pos1[0][i]
			boid.boidslist[i].position[1] = Pos1[1][i]
			boid.boidslist[i].velocity[0] = Vel1[0][i]
			boid.boidslist[i].velocity[1] = Vel1[1][i]
		Pos, Vel, Pos1, Vel1 = Pos1, Vel1, Pos, Vel
		for b in boid.boidslist :
			# b.updateVelocity(x_pos, y_pos, x_vel, y_vel)
			b.draw(win)
		pygame.draw.circle(win, pygame.Color(255,255,0), boid.masscenter, 3)

		pygame.display.flip()

		dt = clock.tick(60) / 1000
		# dt = clock.tick(10) / 1000
		# dt = clock.tick(4) / 1000
		# dt = clock.tick(1) / 1000
		# dt = clock.tick(60) / 1


#	FreeLibrary(dll._handle)
	pygame.quit()
