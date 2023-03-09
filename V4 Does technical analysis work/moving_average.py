"""
Moving averages

@author: Gerhard Kling
"""

import pandas as pd
import numpy as np


"""
Tesco share price
"""
df = pd.read_csv('TSCO.L.csv')

#Use index as a time indicator
df['Time'] = df.index + 1

#Set index - NOTE: you need to reassign
df = df.set_index('Date')

#Pandas plot
df.Close.plot()

"""
Moving average
"""

def moving_average(df, key: str, num_list: list = [50, 200]):
    """    
    Parameters
    ----------
    df: Pandas series
    key: Column name in DataFrame, which defines Series
    num_list: List of number of days to determine MA, 50 and 200 days default

    Returns
    -------
    Adds moving average to DataFrame MA_50, MA_200 by default
    Returns none

    """      
    for num in num_list:
        ma = np.zeros(len(df[key]))
        
        for idx in range(num, len(df[key])):
            ma[idx] = np.mean(df[key].iloc[idx-num:idx])
            
        #Add moving average to DataFrame   
        name = "MA_" + str(num)
        df[name] = ma
        
        #Replace zeros with missing values    
        df[name].iloc[:num].replace(to_replace = 0, value = pd.NA, inplace=True)


"""
Trading signals
"""
#Add moving average to DataFrame   
moving_average(df, 'Close')   

#Plot share price and moving averages    
df.plot(y=['Close', 'MA_50', 'MA_200'])    

#List of our conditions for BUY or SELL signal
conditions = [
    (df.MA_50 > df.MA_200) & (df.MA_50.shift() <= df.MA_200.shift()),
    (df.MA_50 < df.MA_200) & (df.MA_50.shift() >= df.MA_200.shift())
    ]

#List of the values where +1 is BUY and -1 is SELL
values = [1, -1]

#New column in DataFrame using np.select to assign -1 or +1
df['SIGNAL'] = np.select(conditions, values)

#Trade assuming short-selling is not permitted and no transaction costs
#Start with BUY followed by next SELL
buy_time = []
buy_price = []

sell_time = []
sell_price = []

for idx in df.index:
    if df.SIGNAL[idx] == 1:
        buy_time.append(df.Time[idx])
        buy_price.append(df.Close[idx])
    elif df.SIGNAL[idx] == -1:
        sell_time.append(df.Time[idx])
        sell_price.append(df.Close[idx])        
    
#Trades
trades = []        

while len(buy_time) and len(sell_time):    
    #Find first BUY and the subsequent SELL
    min_buy_time = min(buy_time)        
    
    min_sell_time = min(sell_time)     
    
    #BUY signal followed by SELL signal    
    if min_buy_time < min_sell_time: 
        trades.append((buy_price[0], buy_time[0], sell_price[0], sell_time[0]))
        buy_time.pop(0)
        sell_time.pop(0)
        buy_price.pop(0)
        sell_price.pop(0)   
    #Starts with SELL signal, which is ignored (no short-selling)
    else:
        sell_time.pop(0)
        sell_price.pop(0)
        
#Calculate profit
profit = sum([trade[2]-trade[0] for trade in trades])

print(f"You make {round(profit, 0)}")
    
    
    
    