"""
Simulates interest rates
"""

import numpy as np 

class Rate():
    def __init__(self, N=1000, dt=0.05, rho=0.001, alpha=10, gamma=0.04, r0=0.04):
        """
        Parameters
        ----------
        N : Number of steps
        dt : Time steps
        rho : Scale
        alpha : Speed of adjustment
        gamma : Long-term equilibrium
        r0: Current interest rate
        """
        self.N = N
        self.dt = dt
        self.rho = rho
        self.alpha = alpha
        self.gamma = gamma
        self.r0 = r0

    def wiener(self):
        """
        Wiener process
        Returns
        -------
        Array of realisations of Wiener process
        """
        #Result vector
        out = np.zeros(self.N)

        #Initial value
        out[0] = np.sqrt(self.dt) * self.rho * np.random.normal(0, 1)

        for j in range(1, self.N):
            out[j] = out[j - 1] + np.sqrt(self.dt) * self.rho * np.random.normal(0, 1)
            
        return out

    
    def vasicek(self):
        """
        Vasicek (1977) model
        Returns
        -------
        Array of simulated interest rates 
        """        
        #Result vector
        out = np.zeros(self.N)
        
        #Initial value
        out[0] = self.r0
        
        #Wiener process
        w = Rate()
        w = w.wiener()

        for j in range(1, self.N):
            out[j] = out[j - 1] + self.alpha*(self.gamma - out[j - 1])*self.dt + w[j]
            
        return out  


    def cir(self):
        """
        Cox-Ingersoll-Ross Model
        Returns
        -------
        Array of simulated interest rates 
        """        
        #Result vector
        out = np.zeros(self.N)
        
        #Initial value
        out[0] = self.r0
        
        #Wiener process
        w = Rate()
        w = w.wiener()

        for j in range(1, self.N):
            out[j] = out[j - 1] + self.alpha*(self.gamma - out[j - 1])*self.dt + np.sqrt(out[j - 1])*w[j]
            
        return out          