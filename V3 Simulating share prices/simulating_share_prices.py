"""
Simulating share prices

@author: Gerhard Kling
"""

import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

"""
Empirical investigation
"""
df = pd.read_csv('TSCO.L.csv')

#Use index as a time indicator
df['Time'] = df.index + 1

#Set index - NOTE: you need to reassign
df = df.set_index('Date')

#Pandas plot
df.Close.plot()

#Linear regression to obtain drift
mod = smf.ols('Close ~ Time', data=df)
trend = mod.fit()

#Show results and parameters
print(trend.summary())
print(trend.params)

#Add prediction to DataFrame
#Alternative is trend.predict() - but careful with dimensions
df['Trend'] = trend.params[0] + trend.params[1] * df.Time

#Pandas plots share price and trend
df.plot(y=['Close', 'Trend'])

#Take log prices
df['Log_price'] = np.log(df.Close)

#Linear regression with log prices to obtain drift
mod = smf.ols('Log_price ~ Time', data=df)
trend = mod.fit()

#Show results
print(trend.summary())

#Add prediction to DataFrame
df['Log_trend'] = trend.params[0] + trend.params[1] * df.Time

#Pandas plots log share price and trend
df.plot(y=['Log_price', 'Log_trend'])

def share_sim(dx=0.01, p=0.5, dt=0.1, P0=3, N=1000):  
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
        P[idx] = P[idx-1] * np.exp(e[idx])
    
    return P

#Call function and plot simulated share price
P = share_sim()
plt.plot(P)
plt.show()    
    
    