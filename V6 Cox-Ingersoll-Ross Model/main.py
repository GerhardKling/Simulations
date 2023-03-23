"""
V6 Cox-Ingersoll-Ross Model
"""

import matplotlib.pyplot as plt

from rate import Rate

#Initialise rate instance
rate = Rate()

#Apply the CIR method
rate = rate.cir()

#Plot
plt.plot(rate)
plt.show()

