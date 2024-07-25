import random
import statistics
import numpy as np

dice = [0.5, 1.5, 1.05, 1.05, 1.05, 1.05]
pathway = []

# this function will take your wager and multiply it by a random number from dice 300 times straight.
def montecarlo(wager):
    for i in range(0,300):
        portion = wager * 0.4
        remainder = wager * 0.6
        wager = (portion * random.choice(dice)) + remainder
    pathway.append(wager)

# this function will run the function above 10,000 times, such that you get to see the results of 10,000 wagers.
def graphing():
    for i in range(0,100_000):
        montecarlo(1000)

graphing()
print(str("The arithmetic average is: ") + str(statistics.mean(pathway)))
print(str("The geometric average is: ") + str(statistics.geometric_mean(pathway)))
print(str("The median is: ") + str(statistics.median(pathway)))

a = np.array(pathway)
p = np.percentile(a, 5)
print("The fifth percentile is: " + str(p))