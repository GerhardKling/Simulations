"""
V5 Simulating interest rates
"""

import matplotlib.pyplot as plt

from rate import Rate

#Initialise rate instance
rate = Rate()

#Apply Vasicek method
rate = rate.vasicek()

#Plot
plt.plot(rate)
plt.show()

