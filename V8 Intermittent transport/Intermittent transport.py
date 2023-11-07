"""
Intermittent transport
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
s = 0.5

#Persistence probability
p = 0.6

#Change
q = 0.2

#Rest
r = 1-p-q

#Steps
N = 1000

"""
Stochastic evolution equation
"""
#Position array
X = np.zeros(N)
X[0] = X0

#Array of random realisations in [0,1)
w = np.random.rand(N)

#List of history
history = []

#First step
if w[1]<= s:
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
    
    if w[idx]<= p:
        sigma = sigma_k
    elif w[idx]<= p+q:
        sigma = -sigma_k
    else:
        sigma = 0
    
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