"""
Basic simulation
"""


import simpy
import numpy as np
import matplotlib.pyplot as plt 

#Model parameters
#Total number of customers
NUM = 20 

#Probability of arrival
ARR = 0.05

#Collect data
interval = np.zeros(NUM)

#Define process
def purchase(env, arrival = 0.1):
	#Start timer
	minutes = 0
	while True:
		#Generate a probability
		prob = np.random.rand()
		minutes += 1
		print(prob)
		if prob < arrival:
			print(f'Customer number {env.now} arrived.')
			print(f'It took {minutes} minutes.')
			#Add data
			interval[env.now-1] = minutes
			#Reset timer
			minutes = 0
			yield env.timeout(1)

#Create an Environment() instance
env = simpy.Environment()

#Run the process until reaching 20 customers
env.process(purchase(env, arrival = ARR))
env.run(until = NUM + 1)

#Explore data
x = np.arange(NUM)

#Cumulative time
cumulative_time = np.cumsum(interval)

#Bar chart of waiting times
plt.title("Minutes between customers") 
plt.xlabel("Customers") 
plt.ylabel("Interval") 
plt.xticks(range(NUM))
plt.bar(x, interval, color = 'red') 
plt.savefig('CS_arrival.png')
plt.show()