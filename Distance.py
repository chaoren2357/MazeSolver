from math import *
def manhattanDist(x,y):
	s=0
	for xi,yi in zip(x,y):
		s += abs(xi-yi)
	return s
def euclideanDist(x,y):
	s=0
	for xi,yi in zip(x,y):
		s += (xi-yi)**2
	return sqrt(s)	