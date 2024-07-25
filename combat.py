# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import statistics
from matplotlib.gridspec import GridSpec

# 支持中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']



class MonteCarloSimulator:
    def __init__(self, ratio = 1.0,wager=1.0, steps=20, num_simulations=10000):
        self.ratio = ratio
        self.wager = wager
        self.steps = steps
        self.num_simulations = num_simulations
        self.all_returns = []
        print(f"ratio:{self.ratio},wager:{self.wager},steps:{self.steps},num_simulations:{self.num_simulations}")      

    def simulate(self, simulation_func):

        for _ in range(self.num_simulations):
            cash_history = simulation_func(self.ratio,self.wager,self.steps)
            returns = np.array(cash_history)
            self.all_returns.append(returns)

        self.all_returns = np.array(self.all_returns)
        self.mean = np.mean(self.all_returns, axis=0)
        self.median = np.median(self.all_returns, axis=0)
        self.percentile_5 = np.percentile(self.all_returns, 5, axis=0)
        self.percentile_95 = np.percentile(self.all_returns, 95, axis=0)
        
        self.last_median = self.median[-1]
        self.last_pct5 = self.percentile_5[-1]
        self.last_pct95 = self.percentile_95[-1]
        
        return self.last_pct5, self.last_median


def montecarlo_kelly(ratio,wager,steps):
    dice = [1.08,0.84,0.92,2.21,2.62,0.34,1.97,0.87,0.75,1.08,0.92,1.52,1.06,0.89,1.22,0.75,1.36,1.27,0.95,0.78,0.89]
    pathway = [wager]
    for i in range(steps):
        portion = wager * ratio
        remainder = wager * (1-ratio)
        wager = (portion * random.choice(dice)) + remainder
        pathway.append(wager)
    return pathway

def montecarlo_safe(ratio,wager,steps):
    dice = [0.5, 1.5, 1.05, 1.05, 1.05, 1.05]
    pathway = [wager]
    for i in range(steps):
        diceroll = random.choice(dice)
        portion = wager * ratio * diceroll
        if diceroll == 0.5:
            wager = (wager * (1-ratio) * 5) + portion
        else:
            wager = portion
        pathway.append(wager)
    return pathway

def montecarlo_clipped(ratio,wager,steps):
    dice = [1.08,0.95,0.95,1.25,1.25,0.95,1.25,0.95,0.95,1.08,0.95,1.25,1.06,0.95,1.22,0.95,1.25,1.25,0.95,0.95,0.95]
    pathway = [wager]
    for i in range(steps):
        portion = wager * ratio
        remainder = wager * (1-ratio)
        wager = (portion * random.choice(dice)) + remainder
        pathway.append(wager)
    return pathway

def plot_results(medians,pctfives,ratios,steps):
    fig = plt.figure(figsize=(16, 6))
    gs = GridSpec(1, 2, width_ratios=[3, 1.2])

    #不同比例收益率图
    ax1 = fig.add_subplot(gs[0, 0])
    #ax1.set_yscale('log')
    
    ax1.plot(ratios,medians, 'k--', label="中位数收益率")
    ax1.plot(ratios,pctfives, 'k-', label="5分位收益率")
    ax1.set_xlabel('投入比例')
    ax1.set_ylabel('期末收益')
    ax1.set_title('最佳下注比例')
    ax1.legend()
    

    # 创建辅助轴ax2并设置几何平均收益率刻度
    ax2 = ax1.twinx()
    y_min, y_max = ax1.get_ylim()
    ax2.set_ylim(y_min, y_max)
    #ax2.set_yscale('log')
    y_ticks = ax2.get_yticks()

    #yticklabels = [f'{(y**(1/steps)-1)*100:.2f}' if y >= 0 else '0' for y in y_ticks]
    yticklabels = [f'{(y**(1/steps)-1)*100:.2f}' for y in y_ticks]
    print(steps);print(y_ticks); print(yticklabels)
    ax2.set_yticklabels(yticklabels)

    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set_ylabel('几何平均收益率')

    plt.tight_layout()
    plt.savefig("combat.png")
    plt.show()


# 使用 MonteCarloSimulator 类来模拟和绘图
medians=[]
pctfives=[]
ratios = []
lifes = 20
for sample in np.arange(0.1, 1.0, 0.01):
    #simulator = MonteCarloSimulator(ratio = sample, steps=lifes)
    #last_pct5,last_median = simulator.simulate(montecarlo_kelly)
    
    simulator = MonteCarloSimulator(ratio = sample, steps=lifes)
    last_pct5,last_median = simulator.simulate(montecarlo_clipped)
    
    #simulator = MonteCarloSimulator(ratio = sample, steps=lifes)
    #last_pct5,last_median = simulator.simulate(montecarlo_safe)
    pctfives.append(last_pct5)
    medians.append(last_median)
    ratios.append(sample)
print(f"ratios:{ratios}")
print(f"medians:{medians}")
print(f"pctfives:{pctfives}")


plot_results(medians,pctfives,ratios,lifes)