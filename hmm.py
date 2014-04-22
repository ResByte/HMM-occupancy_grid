import numpy as np
import math 
class HMM:
   def __init__(self, A, B, pi):
      assert A.shape[1]==B.shape[0],"A and B are of different dimensions"
      assert pi.shape[0]==A.shape[0],"initial distribution and transition prob matrix are not same"
      self.A = A 
      self.B= B
      self.pi = pi 
   def display(self):
      print self.A
      #print self.B
      #print self.pi

   def train(self, observations, criterion):
      """ Baum-welch algo  (forward backward algo with EM)
		  set theta = (A,B,pi) with random initial conditions
		  this algo find theta* = max(P(Z|theta))
		  Find theta such that it max the probability of the observation
		  Forward Procedure : 
			 let alpha(t) = P(Z1=z1,...Zt = zt,Xt = i | theta)
			 the probability of seeing the obs and being in state i given theta
		  Backward procedure :
			let beta(t) = 
			  
      """
      
      nStates = self.A.shape[0]
      nSamples = len(observations)
      converge = False 
      counter = 0 
      while not converge and counter< 10 :
         counter +=1
         # -----------------------Expectation Step--------------
         #scale factors 
         c = np.zeros(nSamples)
         
         #forward variable
         alpha = np.zeros((nStates,nSamples))
         alpha[:,0] = self.pi*self.B[:, observations[0]] #initialize alpha(1) = pi*b(1st obs)
         c[0]= 1.0/np.sum(alpha[:,0]) # get the first row
         alpha[:,0] = c[0]*alpha[:,0] # normalize first row
         for t in range(1,nSamples): # range start and end
            alpha[:,t]  = np.dot(alpha[:,t-1],self.A)*self.B[:,observations[t]]
            c[t]= 1.0/np.sum(alpha[:,t])
            alpha[:,t]=c[t]*alpha[:,t]
         # Backward variable
         beta = np.zeros((nStates,nSamples))
         beta[:,nSamples-1]=1 # set the last to 1
         #print "c[nsample]"
         #print c[nSamples-1]
         #beta[:,nSamples-1]=c[nSamples-1]*beta[:,nSamples-1]
         #print "beta[nsample-1]"
         #print beta[:,nSamples-1]
         
         for t in range(len(observations)-1,0,-1): # reverse loop
            beta[:,t-1]=np.dot(self.A,(self.B[:,observations[t]]*beta[:,t]))
            beta[:,t-1] = c[t-1]*beta[:,t-1]
         xi = np.zeros((nSamples-1,nStates,nStates)) # joint posterior distribution of current and previous time latent variable
         for t in range(nSamples-1):
            denom = np.dot(np.dot(alpha[:,t].T,self.A)*self.B[:,observations[t+1]].T,beta[:,t+1])
            for i in range(nStates):
               for j in range(nStates):
                  numer = alpha[i,t]*self.A[i,j]*self.B[j,observations[t+1]]*beta[j,t+1]
                  xi[t,i,j] = numer/denom
         #print "Xi"
         #print xi
         gamma = np.sum(xi,axis=2)  # marginal posterior distribution of latent variable
         prod = (alpha[:,nSamples-1]*beta[:,nSamples-1]).reshape((-1,1)).T[0]
         gamma  = np.vstack((gamma, prod/np.sum(prod)))
          
          #----------------------Maximization step--------
          # Update HMM model parameters
         newpi = gamma[0,:]
         newA = np.sum(xi,axis=0)/np.sum(gamma,axis=0).T 
          
         newB = B
         nLevels = self.B.shape[1]
         sumgamma = np.sum(gamma,axis = 0)
         for lev in range(nLevels):
            mask = observations == lev 
            newB[:,lev] = np.sum(gamma[mask,:],axis=0)/sumgamma
          
          # check if converge 
         if np.max(abs(pi-newpi))<criterion and np.max(abs(A-newA)) < criterion and np.max(abs(B-newB)) < criterion:
             converge = True
         self.pi = newpi 
         self.A = newA 
         self.B = newB
          
         HMM.display(self)
if __name__=='__main__':
   pi = np.array([0.5, 0.5])
   A = np.array([[0.5, 0.5],[0.5, 0.5]])
   B = np.array([[0.2, 0.4, 0.4],[0.7, 0.2, 0.1]])
   obs = np.array([0,1,0,1,0,1,2,0,1,0,1,0,1,2,0,1,0])
   hmm=HMM(A,B,pi)
   hmm.train(obs,0.1)
