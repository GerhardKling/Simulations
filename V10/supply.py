"""
Disruption in supply chains
"""
import simpy
import numpy as np
import matplotlib.pyplot as plt 

#Parameters
NUM = 1000

#Collect data
stock = [100]

class Store():
	"""
	Store models stock of rice
	Customers arrive randomly
	"""
	def __init__(self, env):
		"""
		Stock of rice in store and start process
		"""
		self.env = env
		self.stock = 100
		self.start = env.process(self.run())

	def run(self):
		while True:
			#Generate a probability
			prob = np.random.rand()
			if prob < 0.1:
				print(f'Customer number {env.now} arrived.')
				self.stock -= np.random.randint(1, 3)
				print(f'Current stock {self.stock}.')
				stock.append(self.stock)
				yield env.timeout(1)


class Ship():
	def __init__(self, env, store):
		"""
		Refer to environment and start process
		"""
		self.env = env
		self.capacity = 15
		self.start = env.process(self.run(store))

	def run(self, store):
		while True:
			print(f"Ship starts at {env.now}")
			#Waiting until journey completed
			yield env.process(self.on_sea())

			#Ship reached and unloads rice
			store.stock += self.capacity
			print(f"Ship reaches at {env.now}")
			print(f"Store has {store.stock} units of rice.")
			yield env.timeout(1)

	def on_sea(self):
		"""
		Travel time
		"""
		time = np.random.randint(7, 13)
		yield self.env.timeout(time)


class Sim():
	"""
	Sim class initialises the store and ship
	"""
	def __init__(self, env):
		self.env = env
		self.store = Store(self.env)
		self.ship = Ship(env = self.env, store = self.store)

#Create environment and simulation
env = simpy.Environment()
sim = Sim(env)
env.run(until = NUM)

#Line chart of stock
plt.title("Stock of rice in store") 
plt.xlabel("Purchase events") 
plt.ylabel("Stock") 
plt.plot(np.array(stock), color = 'blue') 
plt.savefig('CS_stock.png')
plt.show()