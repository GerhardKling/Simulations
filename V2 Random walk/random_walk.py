"""
Random Walk

@author: Gerhard Kling
"""

import random
import numpy as np
import matplotlib.pyplot as plt

#Parameters
dx = 1 #change in value
p = 0.5 #probability of up movement
dt = 1 #time step
P0 = 10 #initial share price
N = 1000 #number of steps

#White noise process
#Probability from 0 to 1 - steps 0.001
e = np.zeros(N)

for idx in range(N):
    if random.randint(0, 1000)/1000 >= p:
        e[idx] = dx
    else:
        e[idx] = -dx
        
#Simulate share price
P = np.zeros(N)

#Initial value
P[0] = P0

for idx in range(1, N):
    P[idx] = P[idx-1] + e[idx]

#Plot share price
plt.plot(P)
plt.show()    
    
    