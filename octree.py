#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

# ----------------------------------Leaf class -----------------------
class leaf:
	def __init__(self,coord,value,size):
		self.size = size 
		self.coord = coord
		self.value = value

#----------------------------------Node class------------------------
class node:
	def __init__(self,coord,size,parent):
		self.parent = parent 
		self.size = size 
		self.coord = coord
		self.value = 0.5
		#self.center = center
		self.children = [None for i in range(8)]

#-------------------------------------Octree---------------------------
class Octree:
	def __init__(self,worldsize,res):
		world_center = [int(round(worldsize[i]/2)) for i in range(3)]
		self.root = node(world_center,worldsize,None)
		self.worldsize = worldsize
		self.res = res
		self.arr =[] 

	#-------------Find Quadrant --------------------------------
        def findQuadrant(self,coord,center):
                if coord[0] <= center[0]:
                        #negX
                        if coord[1] <= center[1]:
                                #negY
                                if coord[2] <= center[2]:
                                        #negZ
                                        return 6
                                else:
                                        #posZ
                                        return 5
                        else:
                                #posY
                                if coord[2] <= center[2]:
                                        #negZ
                                        return 2
                                else:
                                        #posZ
                                        return 1
                else:
                        #posX
                        if coord[1] <= center[1]:
                                #negY
                                if coord[2] <= center[2]:
                                        #negZ
                                        return 7
                                else:
                                        #posZ
                                        return 4
                        else:
                                #posY
                                if coord[2] <= center[2]:
                                        #negZ
                                        return 3
                                else:
                                        #posZ
                                        return 0

	#-------------------------------Find center of quadrant---------------------
        def findCenter(self,size,center,quadrant):
                newcenter=[0,0,0]
                #print size
                #switch(quadrant){
                if quadrant ==0:
                        for i in range(3):
                                newcenter[i]= size[i]/2 + center[i]
                                return newcenter
                elif quadrant==1:
                        newcenter[0]= -size[0]/2 + center[0]
                        newcenter[1]= size[1]/2 + center[1]
                        newcenter[2]= size[2]/2 + center[2]
                        return newcenter
                elif quadrant == 2:
                        newcenter[0]= -size[0]/2 + center[0]
                        newcenter[1]= size[1]/2 + center[1]
                        newcenter[2]= -size[2]/2 + center[2]
                        return newcenter
                elif quadrant == 3:
                        newcenter[0]= size[0]/2 + center[0]
                        newcenter[1]= size[1]/2 + center[1]
                        newcenter[2]= -size[2]/2 + center[2]
                        return newcenter
                elif quadrant == 4:
                        newcenter[0]= size[0]/2 + center[0]
                        newcenter[1]= -size[1]/2 + center[1]
                        newcenter[2]= size[2]/2 + center[2]
                        return newcenter
                elif quadrant ==5:
                        newcenter[0]= -size[0]/2 + center[0]
                        newcenter[1]= -size[1]/2 + center[1]
                        newcenter[2]= size[2]/2 + center[2]
                        return newcenter
                elif quadrant ==6:
                        newcenter[0]= -size[0]/2 + center[0]
                        newcenter[1]= -size[1]/2 + center[1]
                        newcenter[2]= -size[2]/2 + center[2]
                        return newcenter
                elif quadrant==7:
                        newcenter[0]= size[0]/2 + center[0]
                        newcenter[1]= -size[1]/2 + center[1]
                        newcenter[2]= -size[2]/2 + center[2]
                        return newcenter

	#--------------------------Inverse Sensor Model-------------
	def ISM(self, curr,prev):
		if prev>=0.9 and curr ==1.0:
			return 0.95
		else:
			return 0.5
		
		

	#--------------------------Occupancy update ---------------------
	def occupancyUpdate(self,cur,prev):
		logCur = 5.0
		#logprev = np.log(prev/1-prev)
		logIsm = np.log(self.ISM(int(cur),int(prev))/(1-self.ISM(int(cur),int(prev))))
		update = logCur + logIsm
		print update
		return (1.0-(1.0/(1.0+np.exp(update))))

	#------------------------insert a leaf into tree ---------------

	def add(self,parent,coord,val,size):
		#print size
		#------------------------ find whether the node is of least possible size----------
		if size[0] == self.res or size[1]==self.res or size[2]==self.res:
			# if of lowest size return leaf at that point
			if parent.value != None:
				print parent.value
				parent.value = self.occupancyUpdate(parent.value,1.0)
				print parent.value
				self.arr.append([parent.coord,coord,parent.value])
			else:
				branch = self.findQuadrant(coord,parent.coord)
				parent[branch]= leaf(coord,int(val),res)
				self.arr.append([parent.coord,coord,val])
				
		else:
			#print parent.size
			newsize = [int(round(parent.size[i]/2))  for i in range(3)]
			quad = self.findQuadrant(coord,parent.coord)
			# TODO:newCoord=(some fn)
			newcenter = self.findCenter(newsize , parent.coord , quad)
			 
			if parent.children[quad] is None:
			#	print newsize
				parent.children[quad]= node(newcenter,newsize,parent)
				self.add(parent.children[quad],coord,val,newsize)
			elif isinstance(parent.children[quad],node):
				self.add(parent.children[quad],coord,val,newsize)
	
#	def find(self,coord):	
		

if __name__ == '__main__':
	tree = Octree([640,640,640],1)
	for i in range(10):
		tree.add(tree.root,[i,i*4,i*7],1.0,tree.worldsize)
	print tree.arr
