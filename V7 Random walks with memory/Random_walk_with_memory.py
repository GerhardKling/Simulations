"""
Random walk with memory
@author: Gerhard Kling
"""

import numpy as np
import matplotlib.pyplot as plt 
import random

"""
Parameters
"""
#Initial position
X0 = 0

#First move right (+1)
q = 0.5

#Persistence probability
p = 0.6

#Steps
N = 1000

"""
Stochastic evolution equation
"""
#Position array
X = np.zeros(N)
X[0] = X0

#Array of random realisations in [0,1)
r = np.random.rand(N)

#List of history
history = []

#First step
if r[1]<= q:
    sigma = 1
else:
    sigma = -1
    
#Add to history
history.append(sigma)    

#Evolution at t=0
X[1] = X[0]+sigma

for idx in range(2, N):
    #Random choice from history
    sigma_k = random.choice(history)
    
    if r[idx]<= p:
        sigma = sigma_k
    else:
        sigma = -sigma_k
    
    #Add to history
    history.append(sigma)  

    #Update position
    X[idx] = X[idx-1]+sigma


"""
Plot random walk
"""

steps = np.arange(N) 
plt.title("Random walk with memory") 
plt.xlabel("Steps") 
plt.ylabel("Position") 
plt.plot(steps, X) 
plt.show()