"""Two competing firms: prices, sales and trade-credit repayment risk.

Run: python competition.py
Dependencies: numpy, matplotlib, simpy (python -m pip install numpy matplotlib simpy)
Outputs are written beside this script. No files from trade.py are required.
Prices use integer cents to avoid rounding errors in the repayment test.
"""
from dataclasses import dataclass
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
import simpy


@dataclass(frozen=True)
class Parameters:
    X: int = 50
    p: float = 0.65
    theta: float = 0.80
    tau_t: int = 60
    review_days: int = 5
    discount_cents: int = 5
    floor_cents: int = 80
    cheap_share: float = 0.70


@dataclass
class Firm:
    strategy: str
    inventory: int
    price: int = 100
    cash: int = 0

    def choose_price(self, rival_price, rival_inventory, day, debt, par):
        """Review after today's sales; the new price applies tomorrow."""
        behind_target = self.cash < debt * day / par.tau_t
        if (self.strategy == 'adaptive' and behind_target
                and self.inventory > 0 and rival_inventory > 0):
            return max(par.floor_cents,
                       min(self.price, rival_price - par.discount_cents))
        return self.price


SCENARIOS = [
    ('Both fixed', ('fixed', 'fixed')),
    ('A adaptive; B fixed', ('adaptive', 'fixed')),
    ('Both adaptive', ('adaptive', 'adaptive')),
    ]


def simulate(strategies, par=Parameters(), seed=42, draws=None, record=False):
    """Run to the end of the repayment day, including that day's sales.

    Each day has two independent potential arrivals. Customers observe current
    prices; stockouts redirect them to the other firm. There is no outside option.
    draws contains fixed arrival and customer-choice uniforms (days x 2).
    """
    if (par.X < 1 or par.tau_t < 1 or par.review_days < 1
            or not 0 <= par.p <= 1 or not 0 < par.theta < 1
            or not 0.5 <= par.cheap_share <= 1
            or not 0 < par.floor_cents <= 100 or par.discount_cents <= 0):
        raise ValueError('Invalid model parameters.')
    if len(strategies) != 2 or any(s not in ('fixed', 'adaptive') for s in strategies):
        raise ValueError('Specify two fixed/adaptive strategies.')
    debt_float = 100 * par.theta * par.X
    debt = round(debt_float)
    if not np.isclose(debt, debt_float):
        raise ValueError('Debt must be expressible in whole cents.')
    if draws is None:
        rng = np.random.default_rng(seed)
        draws = (rng.random((par.tau_t, 2)), rng.random((par.tau_t, 2)))
    arrivals, choices = draws
    firms = [Firm(s, par.X) for s in strategies]
    history = np.zeros((par.tau_t + 1, 2, 3)) if record else None
    if record:
        history[0] = [[1, 0, par.X], [1, 0, par.X]]

    def market(env):
        for day in range(1, par.tau_t + 1):
            yield env.timeout(1)
            prices_used = [f.price for f in firms]
            for slot in range(2):
                if arrivals[day - 1, slot] >= par.p:
                    continue
                a, b = firms
                if a.inventory == 0 and b.inventory == 0:
                    continue
                if a.inventory == 0:
                    buyer_choice = 1
                elif b.inventory == 0:
                    buyer_choice = 0
                else:
                    share_a = (0.5 if a.price == b.price else
                               par.cheap_share if a.price < b.price else
                               1 - par.cheap_share)
                    buyer_choice = int(choices[day - 1, slot] >= share_a)
                seller = firms[buyer_choice]
                seller.inventory -= 1
                seller.cash += seller.price
            if record:
                history[day] = [[prices_used[i] / 100, f.cash / 100, f.inventory]
                                for i, f in enumerate(firms)]
            if day % par.review_days == 0 and day < par.tau_t:
                # Calculate both decisions before changing either price.
                new_prices = [f.choose_price(firms[1-i].price,
                              firms[1-i].inventory, day, debt, par)
                              for i, f in enumerate(firms)]
                for f, price in zip(firms, new_prices):
                    f.price = price
        return {'cash': np.array([f.cash / 100 for f in firms]),
                'inventory': np.array([f.inventory for f in firms]),
                'shortfall': np.array([f.cash < debt for f in firms]),
                'history': history, 'debt': debt / 100}

    env = simpy.Environment()
    process = env.process(market(env))
    # Waiting on the process includes day tau_t; a numeric until can exclude it.
    return env.run(until=process)


def experiment(N=10000, par=Parameters(), seed=42):
    """Common random numbers across scenarios, independent replications."""
    if N < 1:
        raise ValueError('N must be positive.')
    rng = np.random.default_rng(seed)
    output = {label: {'cash': np.zeros((N, 2)),
                     'inventory': np.zeros((N, 2)),
                     'shortfall': np.zeros((N, 2), dtype=bool)}
              for label, _ in SCENARIOS}
    for n in range(N):
        draws = (rng.random((par.tau_t, 2)), rng.random((par.tau_t, 2)))
        for label, strategies in SCENARIOS:
            result = simulate(strategies, par, draws=draws)
            for key in output[label]:
                output[label][key][n] = result[key]
    return output


def save_results(output, par, folder):
    rows = []
    for label, _ in SCENARIOS:
        data = output[label]
        for i, firm in enumerate(('A', 'B')):
            probability = data['shortfall'][:, i].mean()
            se = np.sqrt(probability * (1-probability) / len(data['cash']))
            rows.append([label, firm, probability, se,
                         data['cash'][:, i].mean(), data['inventory'][:, i].mean(),
                         data['shortfall'].all(axis=1).mean()])
    with (folder / 'results.csv').open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['scenario', 'firm', 'shortfall_probability', 'MC_SE',
                         'mean_cash', 'mean_inventory', 'both_shortfall_probability'])
        writer.writerows(rows)
    for row in rows:
        print(f'{row[0]:24s} {row[1]}  P(shortfall)={row[2]:.2%} '
              f'MC SE={row[3]:.2%}  mean cash={row[4]:.2f}')

    colors = ['#146C94', '#D05B39']
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False})
    fig, axes = plt.subplots(2, 3, figsize=(12, 6.5), sharex=True,
                             sharey='row', constrained_layout=True)
    for col, (label, strategies) in enumerate(SCENARIOS):
        result = simulate(strategies, par, seed=42, record=True)
        days = np.arange(par.tau_t + 1)
        for i, firm in enumerate(('A', 'B')):
            style = '-' if i == 0 else '--'
            for row in range(2):
                axes[row, col].step(days, result['history'][:, i, row],
                    where='post', color=colors[i], linestyle=style, label=f'Firm {firm}')
        axes[0, col].set_title(label)
        axes[1, col].axhline(result['debt'], color='black', linestyle=':', label='Debt due')
        axes[1, col].set_xlabel('Day')
        axes[0, col].set_ylim(par.floor_cents / 100 - .03, 1.03)
    axes[0, 0].set_ylabel('Selling price (units)')
    axes[1, 0].set_ylabel('Cash before repayment (units)')
    axes[1, 0].legend(loc='upper left', fontsize=8)
    fig.suptitle('One illustrative market path — seed 42; identical customer draws')
    fig.savefig(folder / 'paths.png', dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), constrained_layout=True)
    x = np.arange(len(SCENARIOS))
    for i, firm in enumerate(('A', 'B')):
        probabilities = np.array([output[s]['shortfall'][:, i].mean() for s, _ in SCENARIOS])
        N = len(output[SCENARIOS[0][0]]['cash'])
        # Wilson 95% intervals remain within [0, 1].
        z = 1.96
        centre = (probabilities + z*z/(2*N)) / (1 + z*z/N)
        half = z*np.sqrt(probabilities*(1-probabilities)/N + z*z/(4*N*N))/(1+z*z/N)
        err = np.array([probabilities-centre+half, centre+half-probabilities]) * 100
        axes[0].bar(x+(i-.5)*.34, probabilities*100, width=.34,
                    color=colors[i], label=f'Firm {firm}', yerr=err, capsize=3)
    labels = ['Both\nfixed', 'A adaptive;\nB fixed', 'Both\nadaptive']
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel('Cash-shortfall probability (%)')
    axes[0].set_ylim(0, 100)
    axes[0].set_title('Repayment risk: 95% Monte Carlo intervals')
    axes[0].legend()
    # Empirical CDF of A's cash makes the debt threshold directly interpretable.
    for label, _ in SCENARIOS:
        cash = np.sort(output[label]['cash'][:, 0])
        axes[1].step(cash, np.arange(1, len(cash)+1)/len(cash), where='post', label=label)
    axes[1].axvline(par.theta*par.X, color='black', linestyle=':', label='Debt due')
    axes[1].set_xlabel("Firm A's cash at repayment (units)")
    axes[1].set_ylabel('Cumulative proportion of replications')
    axes[1].set_title('Distribution of cash at the repayment date')
    axes[1].legend(fontsize=8, loc='lower right')
    fig.suptitle(f'{N:,} replications per scenario — illustrative model assumptions')
    fig.savefig(folder / 'risk.png', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    folder = Path(__file__).resolve().parent
    par = Parameters()
    results = experiment(N=10000, par=par, seed=42)
    save_results(results, par, folder)
