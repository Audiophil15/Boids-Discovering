import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from random import randint
from math import *
import pygame

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
	def __init__(self, position =[0.,0.], velocity=[0.,0.], rseek=60, rfollow=40, rflee=20, color=[255,255,255,255]):
		self.id = boid.nextid
		boid.nextid += 1
		self.position = vect(position)
		self.velocity = vect(velocity)
		self.rseek = rseek
		self.rfollow = rfollow
		self.rflee = rflee
		self.color = color
		boid.boidslist.append(self)

	def move(self) :
		self.position += self.velocity

	def updateVelocity(self) :
		# if self == boid.boidslist[0] :
		vel = self.reaction(boid.boidslist)
		# print(vel)
		self.velocity += (self.getSubMassCenter()-self.position).normalize()*0.1
		self.velocity += vel#.normalize()
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
				vel -= v#.normalize()
			elif nv < self.rfollow :
				vel += b.velocity.normalize()*0.2
			elif nv < self.rseek :
				vel += v.normalize()*0.01
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
		if self == boid.boidslist[0] :
			pygame.draw.circle(window, pygame.Color(0,255,255,75), self.position, self.rseek)
			pygame.draw.circle(window, pygame.Color(255,255,0,75), self.position, self.rfollow)
			pygame.draw.circle(window, pygame.Color(255,0,0,75), self.position, self.rflee)
		pygame.draw.circle(window, pygame.Color(*(self.color)), self.position, 3)

if __name__ == "__main__" :

	winsize = [1000, 1000]
	nbboids = 125

	boid([rand()%winsize[0], rand()%winsize[1]], [float(rand()%2),float(rand()%2)], color=(255, 0, 255))
	for i in range(0,nbboids) :
		boid([rand()%winsize[0], rand()%winsize[1]], [float(rand()%2),float(rand()%2)], color=(0,200,int(i/nbboids*200),255)) #-int(i/nbboids*255)

	pygame.init()
	win = pygame.display.set_mode(winsize)
	clock = pygame.time.Clock()
	running = True
	dt = 0

	# sleep(1)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				running = False

		win.fill("black")

		boid.updateGroupMassCenter()
		pygame.draw.circle(win, pygame.Color(255,255,0), boid.masscenter, 3)
		boid.masscenter
		for b in boid.boidslist :
			b.updateVelocity()
			b.draw(win)

		pygame.display.flip()

		dt = clock.tick(60) / 1000

	pygame.quit()

