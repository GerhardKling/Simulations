# Simulations
This repository contains material for the playlist on simulations hosted by YUNIKARN. Visit us on [YouTube](https://www.youtube.com/@YUNIKARN)

# V1: Why do we need simulations - don't we have enough data?
This video introduces our new playlist dedicated to simulations. This is a joint project with our YouTube partner Julian (https://www.youtube.com/c/JulianRighSampedro). This introduction addresses the following questions: (1) Don’t we have enough data? (2) Why are simulations useful? – and (3) What will you learn? In this playlist, we will explore applications in Statistics, Finance, and Physics. Finally, you will learn how to code simulations in various programming languages, including Python, R, Stata, and OpenBugs/WinBugs. Moreover, we need to speed up our code using various methods. 
### [YouTube Video 1](https://youtu.be/3LJlC0thaJc)

# V2: How to simulate a Random Walk in Python?
This video demonstrates the simulation of a random walk in Python. Random walks appear in many disciplines, including Physics and Finance. In the context of Finance, theory suggests that current share prices can be written as the share price in the previous period plus a random process representing public information. We discuss step-by-step the implementation of a Random Walk simulation in Python.

### [YouTube Video 2](https://youtu.be/umgjQlnhrhM)

# V3: How to simulate share prices in Python? 
This video demonstrates the simulation of a share price in Python. Using Yahoo Finance, we look at real financial data and explore drifts in a Random Walk model. Random Walks need to be modified as share prices could become negative. We explore Geometric Brownian Motion and its properties based on Osborne (1959) and Fama (1965). Finally, we implement a simulation in Python that has the desired properties.

### [YouTube Video 3](https://youtu.be/ovpuGg5esO0)

# V4: Can technical analysis predict share prices?
Does technical analysis work? One has to accept that there are theoretical challenges to the idea that technical analysis can be used to predict share prices. In addition, empirical evidence suggests that stock returns are hard to predict. This video illustrates the issues using real financial data. I talk you through an implementation of trading strategies in Python. Using simple moving averages, we will generate trading signals and calculate our profits. Will we succeed? Finally, I will discuss how you can learn more about technical analysis without spending "silly money" on online courses and "special" software. DIY is the way to do it! Let's get ready to code and trade!

## Chapters
- 0:00 Introduction
- 0:32 Theory
- 1:37 Empirical evidence
- 2:34 Financial data
- 3:04 Data import
- 5:24 Simple Moving Average
- 6:29 Trading signals
- 6:54 SMA in Python
- 13:55 Trading signals in Python
- 22:15 Matching trades
- 26:40 Learn Technical Analysis

### [YouTube Video 4](https://youtu.be/cymen-uLiP0)

# V5: How to simulate interest rates in Python?
This video explains the Vasicek (1977) model, which can be used to simulate interest rates. There are many applications in finance and risk management where simulated interest rates can be useful. Vasicek model belongs to the class of one-factor interest rate models. These models have in common that only one factor (the market factor) drives interest rates. I will explain how this model works and how we can implement the model in Python. We will create our own class and two methods. The first method generates a Wiener process and the second method provides simulated interest rates using the Vasicek model.

### [YouTube Video 5](https://youtu.be/339iI58ipOU)

# V6: The Cox-Ingersoll-Ross Model in Python
In a previous video, we developed the Rate class, which enables us to simulate interest rates using the Vasicek (1977) model. We will extend our class by adding a new method that uses the Cox-Ingersoll-Ross Model. The difference is in the stochastic volatility component, which is scaled by the square root of past interest rates. Hence, volatility increases in an environment with high interest rates, which is in line with empirical evidence.

### [YouTube Video 6](https://youtu.be/V76Q38BkILI)

# V7: Random walks with memory
This video explores random walks with memory. This type of stochastic process is sometimes called an elephant random walk. We have a look at these funny random walks proposed by Schuetz and Trimper’s (2004) paper published in Physical Review E. We develop a Python code to simulate these stochastic processes.

### [YouTube Video 7](https://youtu.be/AWCwlEEOslE)

# V8: Intermittent Transport
This video develops a Python script to simulate random walks with memory that permit intermittent transport. This sounds complicated, but it is a modification of the elephant random walk, which I covered in a previous video. The video refers to Kumar, Harbola, and Lindenberg’s (2010) model published in Physical Review E. This is an extension of the random walk with memory based on Schuetz and Trimper’s (2004). This model has many possible applications. Intermittance is very common in financial markets or other settings.

### [YouTube Video 8](https://youtu.be/nDgP9reitj0)

# V9: An introduction to SimPy
This video introduces SimPy, a powerful Python library for building and running simulations in real-time. Data cannot be observed in many applications, or we wish to model rare events (e.g., conflicts, travel bans, etc.). In these cases, simulations might offer valuable insights. I have been using SimPy to model supply chains (e.g., disruption of supply chains, risk management. I will show you how to get started in SimPy by creating a simple demand model. We will learn about events, environments, running processes, and collecting the generated data.

### [YouTube Video 9](https://youtu.be/zybGXgkRUxw)

# V10: Simulating supply chains in SimPy
We attempt to build a more complex supply chain simulation with disruptions. Demand is random, as customers arrive at random times and buy a random number of items. Container ships are used to replenish inventory, but their journey time is a random variable. Various processes and events interact in this simulation. We will create classes and process methods to capture inventory, demand, and supply.

### [YouTube Video 10](https://youtu.be/mFTc0m8sOHE)






