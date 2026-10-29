"""
Trade credit simulation with daily Bernoulli arrivals.

Parameters
----------
X : int
    Initial inventory (units).
p : float
    Daily probability of one customer arriving, 0 < p < 1.
theta : float
    Cost-income ratio, 0 < theta < 1.
tau_t : int
    Trade credit repayment date (days).

Outputs
-------
wait : NumPy array
    Waiting times between customers (days).
S : NumPy array
    Customer arrival times (days).

Assumptions
-----------
Each customer purchases one unit at a price normalised to 1.
Trade credit finances the total production cost, theta * X.
Sales on the repayment date are available for repayment.
"""

import simpy
import numpy as np

# Model parameters
X = 50
p = 0.65
theta = 0.8
tau_t = 60

# Seed for reproducible results
rng = np.random.default_rng(42)


def sale(env, X, p, rng):
    """Simulate daily arrivals until all X units have been sold."""
    arrival_times = []

    while len(arrival_times) < X:
        # Advance one day, whether or not a customer arrives
        yield env.timeout(1)

        if rng.random() < p:
            arrival_times.append(env.now)

    return np.array(arrival_times, dtype=int)


# Create the environment and start the sales process
env = simpy.Environment()
sales_process = env.process(sale(env, X, p, rng))

# Run until inventory is exhausted
S = env.run(until=sales_process)

# Include the wait from day zero to the first customer
wait = np.diff(S, prepend=0)

# Cash available by the end of the repayment date
units_sold = np.count_nonzero(S <= tau_t)
cash_available = units_sold
repayment = theta * X

# Can sales receipts cover the trade credit repayment?
no_risk = cash_available >= repayment

print("Waiting times (days):", wait)
print("Arrival times (days):", S)
print(f"\nAssess cash holdings at the end of day {tau_t}.")
print(f"Units sold: {units_sold}")
print(f"Cash available: {cash_available}")
print(f"Repayment required: {repayment:.2f}")
print(f"Repayment covered: {no_risk}")

def estimate_liquidity_risk(N, X, p, theta, tau_t, seed=42):
    """Estimate the probability that sales cannot cover repayment."""
    rng = np.random.default_rng(seed)
    shortfalls = 0

    for _ in range(N):
        # Start a fresh simulation for each replication
        env = simpy.Environment()
        sales_process = env.process(sale(env, X, p, rng))
        S = env.run(until=sales_process)

        # Include sales on the repayment date
        cash_available = np.count_nonzero(S <= tau_t)
        repayment = theta * X

        if cash_available < repayment:
            shortfalls += 1

    probability = shortfalls / N
    standard_error = np.sqrt(probability * (1 - probability) / N)

    return probability, standard_error


# Baseline estimate
N = 10000
X = 50
p = 0.65
theta = 0.8
tau_t = 60

probability, standard_error = estimate_liquidity_risk(
    N, X, p, theta, tau_t
)

print(f"Replications: {N:,}")
print(f"Estimated probability of a cash shortfall: {probability:.3%}")
print(f"Monte Carlo standard error: {standard_error:.3%}")


# Sensitivity analysis: vary one parameter at a time
scenarios = [
    ("Baseline",       0.80, 0.65, 60),
    ("Lower cost",     0.70, 0.65, 60),
    ("Higher cost",    0.90, 0.65, 60),
    ("Fewer arrivals", 0.80, 0.55, 60),
    ("More arrivals",  0.80, 0.75, 60),
    ("Earlier payment", 0.80, 0.65, 50),
    ("Later payment",   0.80, 0.65, 70),
]

print(
    f"\n{'Scenario':<18} {'theta':>6} {'p':>6} "
    f"{'tau_T':>6} {'P(shortfall)':>14} {'MC SE':>10}"
)

for label, theta_i, p_i, tau_i in scenarios:
    estimate, se = estimate_liquidity_risk(
        N=N,
        X=X,
        p=p_i,
        theta=theta_i,
        tau_t=tau_i,
        seed=42,
    )

    print(
        f"{label:<18} {theta_i:>6.2f} {p_i:>6.2f} "
        f"{tau_i:>6d} {estimate:>14.3%} {se:>10.3%}"
    )