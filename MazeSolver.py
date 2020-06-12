import cv2 
import numpy as np
import os
from Graph import *
from Distance import *
from MazeGenerator import GenerateMaze
from Astar import *

class Maze(Graph):
	def __init__(self,file,mode):
		if mode == "path":
			self.Img = self.readImage(file)
		elif mode == "image":
			self.Img = file
		else:
			raise ValueError("Check your argument mode!")
		self.Digraph = False
		self.analyzeMaze(self.Img)

	def analyzeMaze(self,img):
		i = 0
		while(True):
			if img[i][i] != 0:
				border = i
				break
			i += 1
		i = border
		cell = 0
		while(True):
			if img[i][i] == 0:
				cell = i 
				break
			i += 1
		# if img[cell-border*2][cell] == 0 or img[cell][cell-border*2] == 0:
		# 	cell = cell + border		
		cell = cell + border
		self.Border = border
		self.Cell = cell
		self.Height = int(img.shape[0]/cell)
		self.Width = int(img.shape[1]/cell)
		self.VertexNum = self.Height*self.Width
		self.Visited = [False]*self.VertexNum
		self.EdgeNum = 0
		self.Matrix = [[0]*self.VertexNum for _ in range(self.VertexNum)]
		for i in range(self.Height):
			for j in range(self.Width):
				V = self.transferIndex(i,j)
				for (ni,nj) in self.findNeighbors(img,i,j):
					N = self.transferIndex(ni,nj)
					e = Edge(V,N)
					self.insertEdge(e)
	def transferIndex(self,i,j):
		return i*self.Width+j
		pass

	def transferIndex_reverse(self,num):
		j = num%self.Width
		i = int((num-j)/self.Width)
		return i,j

	def mainPositions(self,row,col):
		up = row*self.Cell
		down = (row+1)*self.Cell-1
		left = col*self.Cell
		right = (col+1)*self.Cell-1
		verticalMid = int((left+right)/2)
		horizontalMid = int((up+down)/2)
		return up,down,left,right,verticalMid,horizontalMid

	def findNeighbors(self,img,row,col):
		neighbors = []
		up,down,left,right,verticalMid,horizontalMid = self.mainPositions(row,col)
		
		if img[horizontalMid][left] != 0:
			neighbors.append((row,col-1))
		if img[horizontalMid][right] != 0:
			neighbors.append((row,col+1))
		if img[up][verticalMid] != 0:
			neighbors.append((row-1,col))
		if img[down][verticalMid] != 0:
			neighbors.append((row+1,col))
		return neighbors

	def show(self,img):
		cv2.imshow('image', img)
		cv2.waitKey(0)		

	def readImage(self,filePath):
		img = cv2.imread(filePath, 0)
		ret, binaryImage = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
		return binaryImage

	def Astar(self,start,end):
		i = 0
		# item in openList:[Point(x,y),F,ParentNode(a,b)]
		openList = [[start,CalculateF(start,end,start),(-1,-1)]]
		closeList = []
		while openList:
			openList.sort(key=lambda x:x[1])
			i+=1
			if end in [i[0] for i in openList]:
				path = [end]
				for item in openList:
					if item[0] == end:
						parent = item[2]
						path.append(parent)
				while parent!=(-1,-1):
					for item in closeList:
						if item[0] == parent:
							parent = item[2]
							path.append(parent)
				path.remove((-1,-1))
				return True,path
			now = openList.pop(0)
			closeList.append(now)
			for node in self.findNeighbors(self.Img,now[0][0],now[0][1]):
				j = 1
				if node in [i[0] for i in closeList]:
					pass
				elif node in [i[0] for i in openList]:
					G_node = CalculateG(start,end,node)
					G_now = CalculateG(start,end,now[0])
					if G_node<G_now:
						for item in openList:
							if item[0] == node:
								openList.remove(item)
						openList.append([node,CalculateF(start,end,node),now[0]])
						openList.sort(key=lambda x:x[1])
				else:
					openList.append([node,CalculateF(start,end,node),now[0]])
		return False,closeList

	def findPath(self,start,end,mode):
		if mode == "Astar":
			_,path = self.Astar(start,end)
			img = self.Img
			for r,c in path:
				img = self.colorCell(img,r,c,150)
		elif mode == "BFS":
			(s1,s2) = start
			(e1,e2) = end
			s = self.transferIndex(s1,s2)
			e = self.transferIndex(e1,e2)
			_ ,path = self.shortestPath_BFS(s,e)
			img = self.Img
			for pos in path:
				r,c = self.transferIndex_reverse(pos)
				img = self.colorCell(img,r,c,150)
		self.show(img)

	def coordinateGlobal2Local(self,x,y):
		r = y//self.Cell
		c = x//self.Cell
		return(r,c)
	def colorCell(self,img,row,col,color):
		img2 = img
		up,down,left,right,verticalMid,horizontalMid = self.mainPositions(row,col)
		for i in range(up,down+1):
			for j in range(left,right+1):
				if img2[i][j] != 0:
					img2[i][j] = color
		return img2



def draw_start_and_end(event,x,y,flags,param):
	global n_g,s_g,e_g
	if event==cv2.EVENT_LBUTTONDOWN :
		if n_g == 0:#首次按下保存坐标值
			n_g+=1
			s_g = (x,y)
			cv2.circle(img,(x,y),2,(0,0,255),-1)
			cv2.putText(img, "start", (x, y), cv2.FONT_HERSHEY_PLAIN,
					1.0, (0, 0, 0), thickness=1)
			cv2.imshow("image", img)
			cv2.waitKey(0)
		elif n_g == 1:#第二次按下显示矩形
			n_g+=1
			e_g = (x,y)
			cv2.circle(img,(x,y),2,(0,0,255),-1)
			cv2.putText(img, "end", (x, y), cv2.FONT_HERSHEY_PLAIN,
					1.0, (0, 0, 0), thickness=1)			
			start = m.coordinateGlobal2Local(s_g[0],s_g[1])
			end = m.coordinateGlobal2Local(e_g[0],e_g[1])
			m.findPath(start,end,"Astar")

if __name__ == '__main__':
	count = [0,0]
	while(1):
		os.system('cls')
		print("1:读取本地迷宫图片")
		print("2:自动生成迷宫")
		print("q:退出")
		mode = input("请输入模式编码：")

		if mode == "q":
			break
		
		elif mode == "1":
			os.system('cls')
			count[0]+=1
			print("这是您读取的第%d张迷宫图片"%count[0])
			print("*****************************************************")
			print("* 提醒：本程序仅支持读取符合下列条件的迷宫：        *")
			print("* 1、迷宫为矩形                                     *")
			print("* 2、迷宫可被划分为等大的正方形子块，且边界厚度固定 *")
			print("*****************************************************")
			filePath = input("如果您的图片符合条件，请输入相对路径;如果不符合，请输入pass继续：")
			if filePath == "pass":
				pass
			else:
				n_g = 0#定义鼠标按下的次数
				s_g = (-1,-1)
				e_g = (-1,-1)
				m = Maze(filePath,"path")
				img = m.Img	
				cv2.namedWindow("image")
				print("单机图片设置起点与终点")
				cv2.setMouseCallback("image", draw_start_and_end)
				cv2.imshow("image", img)
				cv2.waitKey(0)
				
		elif mode == "2":
			count[1]+=1
			print("这是您生成的第%d张迷宫图片"%count[1])
			r = int(input("请输入迷宫的长度："))
			c = int(input("请输入迷宫的宽度："))
			img = GenerateMaze(r,c)
			n_g = 0#定义鼠标按下的次数
			s_g = (-1,-1)
			e_g = (-1,-1)
			m = Maze(img,"image")	
			cv2.namedWindow("image")
			print("单机图片设置起点与终点")
			cv2.setMouseCallback("image", draw_start_and_end)
			cv2.imshow("image", img)
			cv2.waitKey(0)

		else:
			print("输入有误！请重新输入\n")	
		





