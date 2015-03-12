#! /usr/bin/env/python
import numpy as np
import matplotlib.pyplot as plt
import math 
import matplotlib.patches as mpatches
np.set_printoptions(threshold='nan')

currMap = {}

def trainHSMM(x,states,a_0,a_guess,e_guess,d_guess,d_0):
	
	pass

def forwardsHSMM(x,states,a_0,a,e,d,d_0):
	"""
	x = obs seq,duration
	states = list of states 
	a_0 = initial probability
	a = state transition probability 
	e = emmission probability
	d = duration probability
	d_0 = initial duration distribution
	"""

	
	fwd = []
	prev_p = {}
	min_d = 1
	max_d = 5


	for t,x_i in enumerate(x):
		alpha_curr = {}
		bel_curr = {}
		p_curr = {}
		if t ==0:
			for i in states:
				bel_curr[i] = {}
				for di in range(min_d,max_d):	
					bel_curr[i][di] = a_0[i]*d_0[di]

			sum_val = []
			for j in states :
				for dj in range(min_d,max_d):
					sum_val.append(bel_curr[j][dj]*e[j][x_i][dj])
			const_curr = sum(k for k in sum_val)
			for i in states:
				alpha_curr[i] = {}
				for di in range(min_d,max_d):
					alpha_curr[i][di] = (e[i][x_i][di]*bel_curr[i][di])/const_curr
			prev_p = alpha_curr
			fwd.append(alpha_curr)
			#print prev_p					
		else:
			# we first find the belief for curr state
			for i in states:
				bel_curr[i]={}

				for di in range(min_d,max_d):
					sum_val = [] 
					for j in states:
						for dj in range(min_d,max_d):
							if dj == 1 :
								sum_val.append(a[i][j]*d[j][dj]*prev_p[j][dj])
							elif i == j and di == dj-1 : 
								sum_val.append(1*prev_p[j][dj]) # from the assumption that state is changed only at the edges
							else : 
								sum_val.append(0.000001*prev_p[j][dj])
					bel_curr[i][di] = sum(k for k in sum_val)
					print "belief of :",i,di,bel_curr[i][di]
			
			sum_val = []
			for j in states :
				for dj in range(min_d,max_d):
					sum_val.append(bel_curr[j][dj]*e[j][x_i][dj])
			const_curr = sum(k for k in sum_val)		
			print "const_curr :" , const_curr

			maxVal = 0.0
			for i in states:
				alpha_curr[i] = {}
				

				for di in range(min_d,max_d):
					
					alpha_curr[i][di] = (e[i][x_i][di]*bel_curr[i][di])/const_curr
					if maxVal <= alpha_curr[i][di]:
						maxVal = alpha_curr[i][di]
						maxDur = di
						maxstate = i
			print maxVal,maxDur,maxstate


			prev_p = alpha_curr
			fwd.append(alpha_curr)
			#print prev_p
	return fwd


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
		roi = img[1950:2250,1950:2250]
		roi = roi[0:100,0:100]
		value = roi[58][45]

		"""
		cv2.namedWindow('Occupancy grid map',cv2.WINDOW_AUTOSIZE)
		cv2.imshow('Occupancy grid map',roi)
		cv2.waitKey(1000)
		cv2.destroyAllWindows()
		"""
		print "----------------------------------------------------"
		print imageFile
		print "----------------------------------------------------"
		
		for i in xrange(len(roi)-1):
			for j in xrange(len(roi[i])-1):
				if roi[i][j] ==0 or roi[i][j]>=252:
					insert((i,j),roi[i][j]) # insert the observation into current map
		
		return value


if __name__=='__main__':
	sampleFile = sys.argv[1]
	occX =[]
	occY = []
	freeX = []
	freeY = []
	values = []
	with open(sampleFile,'r') as filenames:
		for line in filenames:
			a = line.strip().split()
			values.append(calulatHist(a[0]))
	for i,v in currMap.iteritems():
		print i[0] , " ",i[1]," ",v["occupied"]," ",v["free"]," ",v["prev"]," ",v["occTfree"]," ",v["freeTocc"]," ",v["dur"]
	"""	
	obs_l = 50
	obs = []
	for i in range(5):
		obs.append(0.1)
	for i in range(2):
		obs.append(np.random.normal(0.8,0.05))
	for i in range(3):
		obs.append(0.1)
	for i in range(4):
		obs.append(np.random.normal(0.8,0.05))
	for i in range(16):
		obs.append(0.1)
	for i in range(5):
		obs.append(np.random.normal(0.8,0.05))
	for i in range(2):
		obs.append(0.1)
	for i in range(9):
		obs.append(np.random.normal(0.8,0.05))
	for i in range(5):
		obs.append(0.1)	
	"""

	d_max = 5
	d_min = 1	

	
	'''			
	for i in range(len(obs)):	
		result[i] =np.random.normal(obs[i],5.0)
	#print result	
	'''
	states = ('dynamic','static')
	#end_state = 'static'
	observation = ('Occupied','Free')
	start_probability = {'dynamic': 0.5,'static':0.5}  #with uniform initial probability
	transition_probability = {'dynamic':{'dynamic':0.4,'static':0.6},'static':{'dynamic':0.6,'static':0.4}}
	start_duration_probability  = {1:0.0,2:0.0,3:0.0,4:1.0}
	duration_state_probability ={'dynamic':{1:0.25,2:0.25,3:0.25,4:0.25},'static':{1:0.25,2:0.25,3:0.25,4:0.25}}
	emission_probability = {'dynamic':{'Occupied':{1:0.125,2:0.125,3:0.125,4:0.125},'Free':{1:0.125,2:0.125,3:0.125,4:0.125}},'static':{'Occupied':{1:0.125,2:0.125,3:0.125,4:0.125},'Free':{1:0.125,2:0.125,3:0.125,4:0.125}}} # Heuristically determined 
	ex_observation = []
	for i in obs:
		if i >0.5:
			ex_observation.append('Occupied')
		else:
			ex_observation.append('Free')
	fwdProb = forwardsHSMM(ex_observation,states,start_probability,transition_probability,emission_probability,duration_state_probability,start_duration_probability)		
	

	for i in fwdProb:
		sumval = 0
		for j,k in i.iteritems():
			
			for m,n in k.iteritems():
				#print j,m,n
				sumval = sumval + n
		#print sumval
	
	#calculate MAP of the estimated probabilities
	resSt = []
	resD = []
	for i in fwdProb:
		mxValS = 0.0
		for j,k in i.iteritems():
			mxValD = 0.0
			for m,n in k.iteritems():
				if mxValD < n:
					mxValD = n
					maxD = m
				if mxValD == n:
					maxD = m
			if mxValS <mxValD:
				mxValS = mxValD
				maxS = j
			
		resD.append(maxD)
		if maxS == 'static':
			resSt.append(0.2)
		else:
			resSt.append(0.8)	

	print resSt	
	print resD
	fig = plt.figure()
	#f, axarr = plt.subplots(2, sharex=True)
	#observation = plt.plot([i for i in range(51)],obs,'ro',c = 'r',marker = '+',markersize = 15,label = 'observations')
	resStates = plt.plot([i for i in range(51)],resSt,c = 'b',marker = '.',markersize = 15,label = 'Estimated states')
	#plt.plot([i for i in range(51)],resD,'ro',c = 'g',marker = '2')
	#axarr[0].xlabel('Time stamps')
	#plt.ylabel('Occupancy Probabilities')
	plt.axis([-1,55,0,1.2])
	plt.xlabel('Time stamps')
	plt.ylabel('States')
	#axarr[1].axis([-1,55,0,1.2])
	
	#red_patch = mpatches.Patch(color='g', label='Occupancy grid values')
	#blue_patch = mpatches.Patch(color='blue', label='Observation')
	#blue_line = mlines.Line2D([], [], color='blue', marker='.',
    #                      markersize=15, label='Blue stars')
	plt.legend(loc='upper left')
	#axarr[1].legend(loc='upper left')
	
	#plt.plot(LTM,'r')
	plt.show()
	
	


