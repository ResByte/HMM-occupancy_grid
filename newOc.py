class node:
	def __init__(self, size,center):
		#self.parent = parent
		self.size = size
		self.value = []
		self.center = center
		self.children = [None for i in range(8)]
	
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
			if coord[1] <= self.center[1]:
				#negY
				if coord[2] <= self.center[2]:
					#negZ
					return 7
				else:
					#posZ
					return 4
			else:
				#posY
				if coord[2] <= self.center[2]:
					#negZ
					return 3
				else:
					#posZ
					return 0
	def findCenter(self,size,center,quadrant):
		newcenter=[0,0,0]
		#switch(quadrant){
		if quadrant ==0:
			for i in range(3):
				newcenter[i]= size[i]/2 + center[i]
				return newcenter
		elif quadrant==1:
			newcenter[0]= size[0]/2 - center[0]
			newcenter[1]= size[1]/2 + center[1]
			newcenter[2]= size[2]/2 + center[2]
			return newcenter
		elif quadrant == 2:
			newcenter[0]= size[0]/2 - center[0]
			newcenter[1]= size[1]/2 + center[1]
			newcenter[2]= size[2]/2 - center[2]
			return newcenter
		elif quadrant == 3:
			newcenter[0]= size[0]/2 + center[0]
			newcenter[1]= size[1]/2 + center[1]
			newcenter[2]= size[2]/2 - center[2]
			return newcenter
		elif quadrant == 4:
			newcenter[0]= size[0]/2 + center[0]
			newcenter[1]= size[1]/2 - center[1]
			newcenter[2]= size[2]/2 + center[2]
			return newcenter
		elif quadrant ==5:
			newcenter[0]= size[0]/2 - center[0]
			newcenter[1]= size[1]/2 - center[1]
			newcenter[2]= size[2]/2 + center[2]
			return newcenter
		elif quadrant ==6:
			newcenter[0]= size[0]/2 - center[0]
			newcenter[1]= size[1]/2 - center[1]
			newcenter[2]= size[2]/2 - center[2]
			return newcenter
		elif quadrant==7:
			newcenter[0]= size[0]/2 + center[0]
			newcenter[1]= size[1]/2 - center[1]
			newcenter[2]= size[2]/2 - center[2]
			return newcenter
	def add(self, val, coord, sz):
		print "in adding"
		if sz[0] == 1 or sz[1]==1 or sz[2]==1:
			try:
				self.value.append([coord,val,'leaf'])
			except AttributeError:
				self.value = []
				self.value.append([coord,val,'leaf'])
		else:
			print "size is "
			print sz
			newsize = [int(sz[i]/2) for i in range(3)]
			#Determine quadrant
			quad = self.findQuadrant(coord,self.center)
			newCenter = self.findCenter(newsize,self.center,quad)
			self.children[quad] = node(newsize, newCenter)
			self.children[quad].add(val,coord,newsize)
	def printNode(self):
		if self.size==1:
			print "value of leaf"
			print self.value
			print "coordinate of leaf"
			print self.center
		else:
			for i in self.children:
				if i != None:
					print i.printNode()

class Octree():
    """
    class to hold the whole tree
    """
    
    def __init__(self, world):
        self.world = world
        self.root_coords = [world[0]/2,world[1]/2,world[2]/2]
        self.root = node(world,self.root_coords)

    def add_item(self, payload, coord):
        """
        Create recursively create subnodes until lowest size is reached 
        then deposit payload in that node
        """

        self.root.add(payload, coord, self.world)
    def printTree(self):
		print self.root.printNode()

if __name__ == "__main__":
	print "Creating octree"
	tree = Octree([1000,1000,1000])
	print "inserting node"
	tree.add_item(1, [90,10,10])
	print "Great success"
	tree.printTree()
