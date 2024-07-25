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
    def __init__(self, wager=1.0, steps=300, num_simulations=10000):
        self.wager = wager
        self.steps = steps
        self.num_simulations = num_simulations
        self.all_returns = []

    def simulate(self, simulation_func):
        for _ in range(self.num_simulations):
            cash_history = simulation_func(self.wager, self.steps)
            returns = np.array(cash_history)
            self.all_returns.append(returns)

        self.all_returns = np.array(self.all_returns)
        self.mean = np.mean(self.all_returns, axis=0)
        self.median = np.median(self.all_returns, axis=0)
        self.percentile_5 = np.percentile(self.all_returns, 5, axis=0)
        self.percentile_95 = np.percentile(self.all_returns, 95, axis=0)


    def plot_results(self, name):
        fig = plt.figure(figsize=(16, 6))
        gs = GridSpec(1, 2, width_ratios=[3, 1.2])

        # 第一个子图：收益率路径和统计指标
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_yscale('log')

        for returns in self.all_returns:
            ax1.plot(range(self.steps + 1), returns, color='gray', alpha=0.1)

        ax1.fill_between(range(self.steps + 1), self.percentile_5, self.percentile_95, color='gray', alpha=0.5, label='第5和第95百分位数')
        
        end_returns = self.all_returns[:, -1]
        arithmetic_average = f"平均收益率:{statistics.mean(end_returns):.5f}"
        median_average     = f"中位数收益率:{statistics.median(end_returns):.5f}"
        
        ax1.plot(self.mean, 'k--', label=arithmetic_average)
        ax1.plot(self.median, 'k-', label=median_average)
        ax1.set_xlabel('投掷次数')
        ax1.set_ylabel('收益率')
        ax1.set_title('收益率云团图')
        ax1.legend()

        # 第二个子图：期末收益率的概率密度图
        ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)
        sns.kdeplot(y=self.all_returns[:, -1], ax=ax2, fill=True, color='black')
        ax2.set_xlabel('概率密度')
        ax2.set_title('期末收益率概率密度图')
        ax2.set_ylim(ax1.get_ylim())

        # 创建辅助轴ax3并设置几何平均收益率刻度
        ax3 = ax2.twinx()
        y_min, y_max = ax2.get_ylim()
        ax3.set_ylim(y_min, y_max)
        ax3.set_yscale('log')
        y_ticks = ax3.get_yticks()

        yticklabels = [f'{(y**(1/self.steps)-1)*100:.2f}' for y in y_ticks]
        ax3.set_yticklabels(yticklabels)

        ax3.yaxis.tick_right()
        ax3.yaxis.set_label_position('right')
        ax3.spines['right'].set_position(('axes', 1.0))
        ax3.set_ylabel('几何平均收益率')

        plt.tight_layout()
        plt.savefig(name)
        plt.show()

def montecarlo1(wager, steps):
    dice = [0.5, 1.5, 1.05, 1.05, 1.05, 1.05]
    pathway = [wager]
    for i in range(steps):
        wager = wager * random.choice(dice)
        pathway.append(wager)
    return pathway


def montecarlo2(wager, steps):
    dice = [0.5, 1.5, 1.05, 1.05, 1.05, 1.05]
    pathway = [wager]
    for i in range(steps):
        portion = wager * 0.4
        remainder = wager * 0.6
        wager = (portion * random.choice(dice)) + remainder
        pathway.append(wager)
    return pathway


def montecarlo3(wager, steps):
    dice = [0.5, 1.5, 1.05, 1.05, 1.05, 1.05]
    pathway = [wager]
    for i in range(steps):
        diceroll = random.choice(dice)
        portion = wager * 0.91 * diceroll
        if diceroll == 0.5:
            wager = (wager * 0.09 * 5) + portion
        else:
            wager = portion
        pathway.append(wager)
    return pathway
    

# 使用 MonteCarloSimulator 类来模拟和绘图
simulator1 = MonteCarloSimulator()
simulator1.simulate(montecarlo1)
simulator1.plot_results('montecarlo1.png')

simulator2 = MonteCarloSimulator()
simulator2.simulate(montecarlo2)
simulator2.plot_results('montecarlo2.png')

simulator3 = MonteCarloSimulator()
simulator3.simulate(montecarlo3)
simulator3.plot_results('montecarlo3.png')