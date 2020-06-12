from Distance import *
def CalculateF(s,e,n):
	return manhattanDist(s,n)+manhattanDist(n,e)
def CalculateG(s,e,n):
	return manhattanDist(s,n)
