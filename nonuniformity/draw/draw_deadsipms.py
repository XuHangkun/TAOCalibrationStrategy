import pandas as pd
import matplotlib.pyplot as plt
from utils import generate_dead_sipm, generate_adj_sipm
from tqdm import tqdm

# read dead sipm
output = "../result/nonuniformity/fig/dead_sipm_readout.eps"
data = pd.read_csv("./input/sipm_pos.csv")
dead_list = generate_dead_sipm(seed=8)
dead_data = data.iloc[dead_list,:]
adjs = []
for item in tqdm(dead_list):
    adj_index = generate_adj_sipm(item,data)
    adjs.append(data.iloc[adj_index,:])

# plot sipm
fig = plt.figure()
plt.scatter(data["theta"],data["phi"],label="normal channel",color="blue")
plt.scatter(dead_data["theta"],dead_data["phi"],label="dead channel",color="red")
# for i,d in enumerate(adjs):
#     if i == 0:
#         plt.scatter(d["theta"],d["phi"],label="adjcent channel",color="green",s=1)
#     else:
#         plt.scatter(d["theta"],d["phi"],color="green",s=1)

plt.legend(loc = "upper left")
plt.xlabel("R [mm]",fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("$\\theta [\circ]$",fontsize=16)
plt.tight_layout()
plt.savefig(output)
print("Fig save to %s"%(output))
plt.show()
