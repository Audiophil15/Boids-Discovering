import pyglet
from pyglet import shapes
from random import randint
from math import *

from time import sleep

class vect :
	def __init__(self, list = []) -> None:
		self.coords = list

	def __add__(self, v) :
		if (l:=len(v)) == len(self) :
			return vect([self.coords[0]+v[0], self.coords[1]+v[1]])
			# return vect([ux+vx for ux, vx in zip(self.coords, v)])

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
			d = u[0]*v[0]+u[1]*v[1]
			# for ux, vx in zip(self.coords, v) :
			# 	d += ux*vx
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
		# return vect([ux-vx for ux, vx in zip(self.coords, v)])

	def __str__(self) :
		return str(self.coords)

	def normalize(self) :
		n = norm(self.coords)
		self.coords = vect([self.coords[0]/n, self.coords[1]/n])
		# self.coords = vect([x/n for x in self.coords])
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
		# for c in [0, 1] :
			# if rand()%1000 < 5 :
			# 	self.velocity[c] += 1
			# 	self.velocity[c] %= 3
		# vel = self.reaction(boid.boidslist)
		# print(vel)
		# self.velocity += vel
		# self.velocity = self.velocity/norm(self.velocity)
		# if boid.boidslist[0] is self :
		self.velocity += (self.getSubMassCenter()-self.position).normalize()
			# print(self.position, self.getSubMassCenter(), self.velocity)


		for c in [0, 1] :
			if self.position[c] > 1000 :
				self.velocity[c] = -1
			if self.position[c] < 0 :
				self.velocity[c] = 1
			self.position[c] += (self.velocity[c])*1

	def reaction(self, boidslist) :
		vel = [0.,0.]
		for b in boid.boidslist :
			v = b.position-self.position
			nv = norm(v)
			# if nv < self.rflee :
			# 	vel -= v
			# elif nv < self.rfollow :
			# 	vel += b.velocity
			# elif nv < self.rseek :
			# 	vel += v
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

	def draw(self) :
		shapes.Circle(*(self.position), 3, color=self.color).draw()



if __name__ == "__main__" :

	# v = vect([4,5,6])
	# v += (v-vect([1,2,3])).normalize()
	# print(type(v))
	# v += (v-vect([1,2,3]))
	# v += (v-vect([1,2,3])).normalize()
	# print(v)

	u = [1,0]
	nbboids = 125
	for i in range(0,nbboids) :
		boid([rand()%1000, rand()%1000], [float(rand()%2),float(rand()%2)], color=(0,int(i/nbboids*200),255-int(i/nbboids*255),255))

	winsize = [1000, 1000]

	# print(boid.boidslist)
	# boid.updateGroupMassCenter()
	# print(boid.masscenter)


	window = pyglet.window.Window(*winsize, "Test")
	@window.event
	def on_draw() :
		window.clear()
		boid.updateGroupMassCenter()
		shapes.Circle(*(boid.masscenter), 3, color=(0,255,120,255)).draw()
		for b in boid.boidslist :
			b.draw()
			b.updateVelocity()

	pyglet.app.run()

