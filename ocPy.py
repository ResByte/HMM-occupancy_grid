import numpy as np
import hmm  


def createGrid(size):
	grid = np.zeros([size,size,size])
	return grid  

def trainHMM():
	pass

def main():
	ocGrid = createGrid(100)
	dCube = createGrid(10)
	dcube = [[[1 for x in range(10)]  for x in range(10)] for x in range(10)]
	#shiftCube(ocGrid,dCube,5)
	pi = np.array([0.5, 0.5]) # initial distribution 
	a = np.array([[0.5, 0.5],[0.5, 0.5]]) # State transition matrix
	b = np.array([[0.2, 0.4, 0.4],[0.7, 0.2, 0.1]]) # Observation matrix
	obs = np.array([0,1,0,1,0,1,2,0,1,0,1,0,1,2,0,1,0])
	hdmm=hmm.HMM(a,b,pi)
	hdmm.train(obs,0.1)
	#print dcube

if __name__ == '__main__':
	#print "in main"
	main()

