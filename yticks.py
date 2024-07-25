import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5, 6,7,8,9], [-0.5,0.,0.5 ,1.,1.5 , 2.,2.5 ,3.,3.5])

y_ticks = ax.get_yticks()
#yticklabels = [f'{y**(1/20):.2f}' for y in y_ticks]
yticklabels = [f'{y**(1/20):.2f}' if y >= 0 else '0' for y in y_ticks]
print(y_ticks);print(yticklabels)
print(type(y_ticks))