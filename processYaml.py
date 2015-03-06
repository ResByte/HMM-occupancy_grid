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


def insert(point,val):
	#print "Inserting values for point", point
	flag = True
	for i,v in currMap.iteritems():
		if i == point:
			if val == 0:
				#print max(v["occupied"],v["free"])
				v["occupied"] += 1
				if v["prev"] == "free":
					v["freeTocc"] += 1
					#print "free to occ :", v["freeTocc"]
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
					#print "occ to free :",v["occTfree"]
					v["dur"] = 1
				if v["prev"] == "free":
					v["dur"] +=1
				v["prev"] = "free"
				flag = False
	#print "length of curr map ",len(currMap)	
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
		roi = roi[150:250,30:130]
		"""
		cv2.namedWindow('Occupancy grid map',cv2.WINDOW_AUTOSIZE)
		cv2.imshow('Occupancy grid map',roi)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		
		print "----------------------------------------------------"
		print imageFile
		print "----------------------------------------------------"
		"""
		for i in xrange(99):
			for j in xrange(99):
				if roi[i][j] ==0 or roi[i][j]>=252:
					insert((i,j),roi[i][j]) # insert the observation into current map




	
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
	for i,v in currMap.iteritems():
		print i[0] , " ",i[1]," ",v["occupied"]," ",v["free"]," ",v["prev"]," ",v["occTfree"]," ",v["freeTocc"]," ",v["dur"]
	"""
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
	"""		
	

if __name__ == '__main__':
	main()
