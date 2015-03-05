#!/usr/bin/env python
from yaml import load 
import numpy as np 
import sys 
import cv2
import matplotlib.pyplot as plt

allOccPoints = []
allStaticPoint =[]
currMap = {}
priorMap = []

"""
def sequentialSearch(newMap):
	
	Input: image of the occupancy grid from yaml 
	
	for i in xrange(len(newMap)):
		for j in xrange(len(newMap[i])):
"""
def forwards(x,states,a_0,a,e):
	"""
	This is a forwards algorithm for Hidden Markov Model. 
	Assumption: State transition probability(a), initial state probability(a_0) and observation probability(e) are known. 
	Goal: Comput the marginal posterior p(z_t | x_1:t)
	alpha = joint probability posterior 
	p_curr = marginal posterior probability 
	The algorithm is from Murphy et al. (Machine Learning a probabilistic approach)
	"""
	#control undeflow
	L = len(x) #length of observation
	fwd = []
	alpha_prev = {}
	const_prev = {}
	p_prev = {}
	for i, x_i in enumerate(x):
		alpha_curr = {}
		bel_curr = {}
		p_curr={}
		for st in states:
			if i != 0:
				bel_curr[st]=sum(a[k][st]*p_prev[k] for k in states) # Estimate belief of the states from previous estimates
		for st in states:
			if i == 0:
				
				const_curr = sum(a_0[s0]*e[s0][x_i] for s0 in states) #constant for normalization initializer
				alpha_curr[st] = (a_0[st]*e[st][x_i])
			else:
				
				const_curr = sum(bel_curr[k]*e[k][x_i] for k in states)
				alpha_curr[st] =e[st][x_i]*(sum(alpha_prev[k]*a[k][st] for k in states))
			p_curr[st] = alpha_curr[st]/const_curr

		fwd.append(p_curr)
		alpha_prev = alpha_curr
		p_prev = p_curr
	return fwd
	
	
def nearestNeigbour(point,ptList):
	"""
	Search for the sampe point in the vicinity because of inherent noise in sensor
	"""
	for i in xrange(4):
		for j in xrange(4):
			if [point[0]+i -2 ,point[1]+j -2] in ptList:
				return True
	return False

def insert(point,val):
	flag = True
	for i,v in currMap.iteritems():
		if i == point:
			if val == 0:
				#print max(v["occupied"],v["free"])
				v["occupied"] += 1
				if v["prev"] == "free":
					v["freeTocc"] += 1
					print "free to occ :", v["freeTocc"]
					v["dur"] = 1
				if v["prev"] == "occupied":
					v["dur"] +=1
				v["prev"] = "occupied"
				flag = False
			if val >= 252:
				#print max(v["occupied"],v["free"])
				
				v["free"] += 1
				if v["prev"] == "occupied":
					v["occTfree"] += 1
					print "occ to free :",v["occTfree"]
					v["dur"] = 1
				if v["prev"] == "free":
					v["dur"] +=1
				v["prev"] = "free"
				flag = False
		
	if val == 0 and flag:
		currMap[(point[0],point[1])] = {"occupied":1,"free":0,"prev":"occupied","occTfree":0,"freeTocc":0,"dur":1}
	if val >252 and flag:
		currMap[(point[0],point[1])] = {"occupied":0,"free":1,"prev":"free","occTfree":0,"freeTocc":0,"dur":1}		 



def calulatHist(yamlFile):
	
	with open(yamlFile,'r') as dataFile:
		doc = load(dataFile)
		imageFile = doc['image']
		img = cv2.imread(imageFile,cv2.IMREAD_UNCHANGED)
		roi = img[1900:2250,1950:2250]
		roi = roi[30:280,20:300]
		print imageFile
		for i in xrange(len(roi)-1):
			for j in xrange(len(roi[i])-1):
				insert((i,j),roi[i][j]) # insert the observation into current map




				
def plotData(yamlFile,prevOcc):
	occPointsX = []
	occPointsY = []
	#cv2.namedWindow('Occupancy grid map',cv2.WINDOW_AUTOSIZE)
	allocc =[]
	dyX =[]
	dyY = []
	staticX	=[]
	staticY = []
	with open(yamlFile,'r') as dataFile:
		doc = load(dataFile)
		imageFile =  doc['image']
		img = cv2.imread(imageFile,cv2.IMREAD_UNCHANGED) # without changing the original occupancy grid
		print img.shape
		print img.size
		roi = img[1900:2250,1950:2250]
		roi =roi[30:280,30:300] 		# roi is extracted from the image
		

		for i in xrange(len(roi)-1):
			for j in xrange(len(roi[i])-1):
				if roi[i][j] == 0 :

					occPointsX.append(i)
					occPointsY.append(j)
					allocc.append([i,j])
					#print roi[i][j]

					
	#print len(occPointsX)	
	for i in xrange(len(occPointsX)-1):
		if not nearestNeigbour([occPointsX[i],occPointsY[i]],prevOcc) :
			dyX.append(occPointsX[i])
			dyY.append(occPointsY[i])
		else :
			staticX.append(occPointsX[i])
			staticY.append(occPointsY[i]) 
	

	"""		

	for i in xrange(len(staticX)-1):
		if not nearestNeigbour([staticX[i],staticY[i]],allStaticPoint):
			allStaticPoint.append([staticX[i],staticY[i]])		

	fig = plt.figure()
	#axSt= plt.subplot(2,2,1)
	axSt = plt.gca()
	axSt.scatter(staticX,staticY,c= "#0000ff",marker = ',',alpha = 0.5)
	
	#axDy = plt.subplot(2,2,2)
	#axDy.scatter(dyX,dyY,marker = ',',alpha = 0.5)
	axSt.scatter(dyX,dyY,c="#ffffff",marker = ',',alpha = 0.5)
	
	plt.hold(True)
	plt.show()	
	"""		
	#cv2.imshow('Occupancy grid map',roi)
	#cv2.waitKey(3)
	#cv2.destroyAllWindows()
	return allocc


	
def main():
	sampleFile = sys.argv[1]
	occX =[]
	occY = []
	freeX = []
	freeY = []
	with open(sampleFile,'r') as filenames:
		for line in filenames:
			a = line.strip().split()
			calulatHist(a[0])
	print len(currMap)
	for i,v in currMap.iteritems():
		tmp = -1
		for j,k in v.iteritems():
			if tmp < k:
				tmp = k
				state = j
		if state == "occupied":
			occX.append(i[0])
			occY.append(i[1])
		if state == "free":
			freeX.append(i[0])
			freeY.append(i[1])

	print len(freeX)

	fig = plt.figure()
	ax= fig.gca()
	ax.scatter(freeX,freeY,marker = ',',alpha = 0.5)
	plt.hold(True)
	plt.show()		
	

if __name__ == '__main__':
	main()
