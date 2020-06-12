# from Graph import *
# from Queue import *
import random
import numpy as np


def GenerateMaze(num_rows,num_cols):


	M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)
	cell = 20
	border = 2
	image = np.zeros((num_rows*cell,num_cols*cell), dtype=np.uint8)
	 
	# Set starting row and column
	r = 0
	c = 0
	history = [(r,c)]
	while history: 
		r,c = random.choice(history)
		M[r,c,4] = 1 
		history.remove((r,c))
		check = []

		if c > 0:
			if M[r,c-1,4] == 1:
				check.append('L')
			elif M[r,c-1,4] == 0:
				history.append((r,c-1))
				M[r,c-1,4] = 2
		if r > 0:
			if M[r-1,c,4] == 1: 
				check.append('U') 
			elif M[r-1,c,4] == 0:
				history.append((r-1,c))
				M[r-1,c,4] = 2
		if c < num_cols-1:
			if M[r,c+1,4] == 1: 
				check.append('R')
			elif M[r,c+1,4] == 0:
				history.append((r,c+1))
				M[r,c+1,4] = 2 
		if r < num_rows-1:
			if M[r+1,c,4] == 1: 
				check.append('D') 
			elif  M[r+1,c,4] == 0:
				history.append((r+1,c))
				M[r+1,c,4] = 2
	 
		if len(check):
			move_direction = random.choice(check)
			if move_direction == 'L':
				M[r,c,0] = 1
				c = c-1
				M[r,c,2] = 1
			if move_direction == 'U':
				M[r,c,1] = 1
				r = r-1
				M[r,c,3] = 1
			if move_direction == 'R':
				M[r,c,2] = 1
				c = c+1
				M[r,c,0] = 1
			if move_direction == 'D':
				M[r,c,3] = 1
				r = r+1
				M[r,c,1] = 1
	         

	for row in range(0,num_rows):
		for col in range(0,num_cols):
			cell_data = M[row,col]
			for i in range(cell*row+border,cell*(row+1)-border):
				image[i,range(cell*col+border,cell*(col+1)-border)] = 255
			if cell_data[0] == 1: 
				for cp in range(border):
					image[range(cell*row+border,cell*(row+1)-border),cell*col+cp] = 255
			if cell_data[1] == 1: 
				for rp in range(border):
					image[cell*row+rp,range(cell*col+border,cell*(col+1)-border)] = 255
			if cell_data[2] == 1: 
				for cp in range(border):
					image[range(cell*row+border,cell*(row+1)-border),cell*(col+1)-border+cp] = 255
			if cell_data[3] == 1: 
				for rp in range(border):
					image[cell*(row+1)-border+rp,range(cell*col+border,cell*(col+1)-border)] = 255


			# if cell_data[0] == 1 and cell_data[1] == 1:
			# 	for cp in range(border):
			# 		for rp in range(border):
			# 			image[cell*row+rp,cell*col+cp] = 255
			# if cell_data[1] == 1 and cell_data[2] == 1:
			# 	for cp in range(border):
			# 		for rp in range(border):
			# 			image[cell*row+rp,cell*(col+1)-border+cp] = 255				
			# if cell_data[2] == 1 and cell_data[3] == 1:
			# 	for cp in range(border):
			# 		for rp in range(border):
			# 			image[cell*(row+1)-border+rp,cell*(col+1)-border+cp] = 255						
			# if cell_data[3] == 1 and cell_data[0] == 1:
			# 	for cp in range(border):
			# 		for rp in range(border):
			# 			image[cell*(row+1)-border+rp,cell*col+cp] = 255	
	return image

# img = GenerateMaze(10,10)
# cv2.namedWindow('image')
# cv2.imshow('image',img)
# cv2.waitKey(0)
