from MazeSolver import *
from MazeGenerator import GenerateMaze
# for i in range(5):
# 	img = GenerateMaze(10,10)
# 	cv2.imwrite("maze0"+str(i)+".jpg",img)
# for i in range(5):
# 	img = GenerateMaze(20,20)
# 	cv2.imwrite("maze1"+str(i)+".jpg",img)
filePath = "maze00.jpg"
m = Maze(filePath,"path")
print(m.findPath((0,0),(9,9),"Astar"))