import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

# Read data
data = pd.read_csv("./input/energy_resolution.csv")
x = data["energy"].to_numpy()
y = data["all"].to_numpy()
plt.scatter(x,y)

methods = ["linear","quadratic","cubic"]
xx = np.arange(1.3,13,0.2)
for method in methods:
    f = interpolate.interp1d(x, y,kind=method)
    yy = f(xx)
    plt.plot(xx,yy,label=method)
plt.legend()
plt.ylim(0,0.02)
plt.show()
