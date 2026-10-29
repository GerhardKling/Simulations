"""
Basic simulation
"""

import simpy
import numpy as np
import matplotlib.pyplot as plt 

"""
Model parameters
n_max: Integer: Total number of customers
arrival: Float: Arrival probability of customers
wait: NumPy array: Simulated waiting times
"""
n_max = 50 
arrival = 0.05
wait = np.zeros(n_max)

def sale(env, arrival):
	minutes = 0
	customer = 0
	"""
	Arguments:
	env: environment instance
	arrival: arrival probability: model parameter
	"""
	while customer < n_max:
		# Advance the simulation by one minute
		yield env.timeout(1)
		minutes += 1

		# Check whether a customer arrives this minute
		if np.random.rand() < arrival:
			wait[customer] = minutes
			customer += 1

			print(f'Customer number {customer} arrived '
					f'at minute {env.now}.')
			print(f'It took {minutes} minutes.')

			minutes = 0

#Creating an environment instance
env = simpy.Environment()

#Run the process
env.process(sale(env, arrival = arrival))
env.run()

#Data visualisation
x = np.arange(n_max)

#Figure of waiting times
plt.title("Time between customers") 
plt.xlabel("Customers") 
plt.ylabel("Interval") 
plt.xticks(ticks = np.arange(0, len(x), 5))
plt.bar(x, wait, color = 'red') 
plt.savefig('wait.png')
plt.show()



