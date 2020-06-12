from math import *
from Queue import *
class Edge(object):
	'''
	Edge of graph in data structure.
	'''
	def __init__(self,V1,V2,Weight=1):
		self.V1=V1 
		self.V2=V2
		self.Weight=Weight

		
class Graph(object):
	def __init__(self,VertexNum=0,Digraph = False):
		self.VertexNum = VertexNum
		self.Matrix = [[float("inf")]*VertexNum for _ in range(VertexNum)] 
		self.Visited = [False]*self.VertexNum
		self.Digraph = Digraph
		self.EdgeNum = 0
	def insertEdge(self,E):
		if isinstance(E,tuple):
			(r,c,w) = E
			E = Edge(r,c,w)
		if self.Digraph:
			self.Matrix[E.V1][E.V2] = E.Weight
		else:
			self.Matrix[E.V1][E.V2] = E.Weight
			self.Matrix[E.V2][E.V1] = E.Weight
		self.EdgeNum+=1
	def isConnect(self,v1,v2):
		return self.Matrix[v1][v2] is not 0
		pass
	def near(self,v):
		N = []
		for i in range(self.VertexNum):
			if(self.isConnect(v,i)):
				N.append(i)
		return N
	def resetVisited(self):
		self.Visited = [False]*self.VertexNum	
		pass
	def dFS(self,v,resetVisited = False):
		'''from vertex v deep first search graph G
		'''
		print("Now visit ",v)
		self.Visited[v] = True
		for w in self.near(v):
			if (not self.Visited[w]):
				self.dFS(w)
		if(resetVisited):
			self.resetVisited()
	def bFS(self,v,resetVisited = False):
		'''from vertex v breadth first search graph G
		'''
		print("Now visit ",v)
		self.Visited[v] = True
		Q = Queue()
		Q.addQueue(v)
		while(not Q.isEmpty()):
			V = Q.popOut()
			for w in self.near(V):
				if(not self.Visited[w]):
					print("Now visit ",w)
					self.Visited[w] = True
					Q.addQueue(w)
		if(resetVisited):
			self.resetVisited()
	def shortestPath_BFS(self,start,end = -1):
		'''find the shortest path from vertex v to any other vertex in graph G
		'''
		dist = [-1]*self.VertexNum
		path = [-1]*self.VertexNum
		dist[start] = 0
		Q = Queue()
		Q.addQueue(start)
		while(not Q.isEmpty()):
			V = Q.popOut()
			for w in self.near(V):
				if(dist[w] == -1):
					dist[w] = dist[V] +1
					path[w] = V 
					Q.addQueue(w)
		if end>=0:
			dist = dist[end]
			p = []
			node = end
			while(node != -1):
				p.append(node)
				node = path[node]
			p.reverse()
			path = p
		return dist,path
	def Dijkstra(self,start):		
		collected = [False]*self.VertexNum
		dist = self.Matrix[start]
		path = [-1 if x == float("inf") else start for x in self.Matrix[start]]
		dist[start] = 0
		collected[start] = True
		while(1):
			V = self.findMinDist(dist,collected)
			if V == False:
				break
			collected[V] = True
			for W in range(self.VertexNum):
				if (collected[W] == False and self.Matrix[V][W] < float("inf")):
					if self.Matrix[V][W]<0:
						return False,dist,path
					if dist[V]+self.Matrix[V][W] < dist[W]:
						dist[W] = dist[V]+self.Matrix[V][W]
						path[W] = V
		return True,dist,path
	def findMinDist(self,dist,collected):
		MinDist = float("inf")
		for V in range(self.VertexNum):
			if(collected[V] == False and dist[V]<MinDist):
				MinDist = dist[V]
				MinV = V
		if MinDist < float("inf"):
			return MinV
		else:
			return False


