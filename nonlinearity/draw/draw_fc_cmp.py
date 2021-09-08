import matplotlib.pyplot as plt
import numpy as np
import copy
from matplotlib import gridspec
import sys
import pickle
import ROOT
import os
import pandas as pd

# plot ana cal
cov = pd.read_csv("./input/TAO_Cherenkov.csv")
norm = 1.0
plt.plot(cov["energy"].to_numpy(),cov["energy"].to_numpy()*cov["cov"].to_numpy()/norm,linewidth=2.5)
plt.xlabel("$E^{e}$ [MeV]",fontsize=16)
plt.ylabel("$f_{C}$ [a.u.]",fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.yscale("log")
plt.ylim(1.e-2,5.e1)
plt.xlim(0,13)
plt.tight_layout()
fig_path = "../result/nonlinearity/fig/Cherenkov_template.eps"
plt.savefig(fig_path)
print("Fig save to %s"%(fig_path))
plt.show()

