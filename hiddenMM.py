import numpy as np
import matplotlib.pyplot as plt

def forwardBackward(x,states,a_0,a,e,end_st):
	"""
	This is a forward-backward algorithm for inference in Hidden Markov Model.
	Assumption: The state transition probabilities, initial state probabilities and 
	observation probabilities are known. 
	Goal: Estimate the posterior probability of a state given observation and parameters.
	Computational Complexity is Big-Oh(number of observations * square of number of states)
	in case of finate states it is linear.
	"""
	L = len(x) #length of observation
	fwd = []
	f_prev = {}

	for i, x_i in enumerate(x):
		f_curr = {}
		for st in states: 
			if i == 0:
				prev_f_sum = a_0[st] # for the first term
			else:
				prev_f_sum = sum(f_prev[k]*a[k][st] for k in states) # update equation for forward algorithm 

			f_curr[st] = e[st][x_i]*prev_f_sum
		fwd.append(f_curr)
		f_prev = f_curr
	p_fwd = sum(f_curr[k]*a[k][end_st] for k in states)

	bkw = []
	b_prev ={}
	for i, x_i_plus in enumerate(reversed(x[1:]+(None,))):
		b_curr = {}
		for st in states :
			if i ==0:
				b_curr[st] = a[st][end_st] # last term update
			else:
				b_curr[st] = sum(a[st][l]*e[l][x_i_plus]*b_prev[l] for l in states) # update equation for backward algorithm

		bkw.insert(0,b_curr)
		b_prev = b_curr
	p_bkw = sum(a_0[l]*e[l][x[0]]*b_curr[l] for l in states)

	posterior =[]
	for i in xrange(L):
		posterior.append({st: fwd[i][st]*bkw[i][st]/p_fwd for st in states}) # calculating poseterior at each observation
	assert p_fwd == p_bkw
	return fwd,bkw,posterior

def forwards(x,states,a_0,a,e,end_state):
	"""
	This is a forwards algorithm for Hidden Markov Model. 
	Assumption: State transition probability(a), initial state probability(a_0) and observation probability(e) are known. 
	Goal: Comput the marginal posterior p(z_t | x_1:t)
	alpha = joint probability posterior 
	p_curr = marginal posterior probability 
	The algorithm is from Murphy et al. (Machine Learning a probabilistic approach)
	"""
	#TODO: Not accurate 
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
	
	for i in fwd:
		print max(i[k] for k in states)


def viterbi(x,states,a_0,a,e):
	V= [{}]
	path = {}

	for y in states:
		V[0][y] = a_0[y]*e[y][x[0]]
		path[y] = [y]

	for t in xrange(1,len(x)):
		V.append({})
		newpath = {}

		for y in states:
			(prob,state) = max((V[t-1][y0]*a[y0][y]*e[y][x[t]],y0)for y0 in states )
			V[t][y] = prob
			newpath[y] = path[state] + [y]
		path = newpath
	n=0
	if len(x) != 1:
		n = len(x)-1	
	(prob,state) = max((V[n][y],y) for y in states)
	print (prob, path[state])	


if __name__ == '__main__':
	states = ('dynamic','static')
	end_state = 'static'
	observation = ('Occupied','Free','Unknown')
	start_probability = {'dynamic': 0.5,'static':0.5}  #with uniform initial probability
	transition_probability = {'dynamic':{'dynamic':0.5,'static':0.5},'static':{'dynamic':0.5,'static':0.5}}
	emission_probability = {'dynamic':{'Occupied':0.5,'Free':0.4,'Unknown':0.1},'static':{'Occupied':0.8,'Free':0.1,'Unknown':0.1}} # Heuristically determined 
	ex_observation = ('Free','Free','Free','Free','Free','Occupied','Occupied','Occupied','Occupied','Unknown','Occupied','Free','Occupied','Occupied','Occupied','Occupied')
	#fwd_pr,bkw_pr, posterior_pr = forwardBackward(ex_observation,states,start_probability,transition_probability,emission_probability,end_state)
	forwards(ex_observation,states,start_probability,transition_probability,emission_probability,states[0])
	#print ex_observation
	#viterbi(ex_observation,states,start_probability,transition_probability,emission_probability)

