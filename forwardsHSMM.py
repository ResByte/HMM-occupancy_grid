import sys
import numpy as np


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
	print fwd

if __name__ == '__main__':
	states = ('dynamic','static')
	#end_state = 'static'
	observation = ('Occupied','Free')
	start_probability = {'dynamic': 0.5,'static':0.5}  #with uniform initial probability
	transition_probability = {'dynamic':{'dynamic':0.5,'static':0.5},'static':{'dynamic':0.5,'static':0.5}}
	start_duration_probability  = {1:0.2,2:0.2,3:0.2,4:0.2,5:0.2}
	duration_state_probability ={'dynamic':{1:0.2,2:0.2,3:0.3,4:0.2,5:0.2},'static':{1:0.2,2:0.2,3:0.3,4:0.2,5:0.2}}
	emission_probability = {'dynamic':{'Occupied':{1:0.1,2:0.1,3:0.1,4:0.1,5:0.1},'Free':{1:0.1,2:0.1,3:0.1,4:0.1,5:0.1}},'static':{'Occupied':{1:0.1,2:0.1,3:0.1,4:0.1,5:0.1},'Free':{1:0.1,2:0.1,3:0.1,4:0.1,5:0.1}}} # Heuristically determined 
	ex_observation = ('Free','Free','Free','Free','Free','Occupied','Occupied','Occupied','Occupied','Occupied','Free','Occupied','Occupied','Occupied','Occupied')
	#fwd_pr,bkw_pr, posterior_pr = forwardBackward(ex_observation,states,start_probability,transition_probability,emission_probability,end_state)
	forwardsHSMM(ex_observation,states,start_probability,transition_probability,emission_probability,duration_state_probability,start_duration_probability)
	#print ex_observation
	#viterbi(ex_observation,states,start_probability,transition_probability,emission_probability)



