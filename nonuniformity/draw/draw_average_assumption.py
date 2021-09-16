import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from utils import generate_dead_sipm, generate_adj_sipm
from tqdm import tqdm
from TaoDataAPI import TAOData
import numpy as np

# load sipm data, dead readout channels and its adjcent
data = pd.read_csv("./input/sipm_pos.csv")
dead_list = generate_dead_sipm(seed=8)
adjs = []
for item in tqdm(dead_list):
    adj_index = generate_adj_sipm(item,data)
    f_indexs = []
    for j in adj_index:
        if j not in dead_list:
            f_indexs.append(j)
    adjs.append(f_indexs)

# load electron data
files = ["../../offline/change_data/nonuniformity/electron/electron_4.0MeV_theta0_r602.root"]
# files = ["../../offline/change_data/nonuniformity/electron/electron_1.0MeV_theta0_r0.root"]
e_data = TAOData(files)
e_data.SetBranchStatus(["*"],0)
e_data.SetBranchStatus(
                ["fGdLSEdep","fGdLSEdepX","fGdLSEdepY","fGdLSEdepZ","fNSiPMHit","fPrimParticleKE","fSiPMHitID"],1)

info = {"total_true":[],"total_pred":[],"total_unc":[]}
for i in dead_list:
    info[i] = {"true":[],"pred":[]}

for i in tqdm(range(e_data.GetEntries())):
    e_data.GetEntry(i)
    nhit = e_data.GetAttr("fNSiPMHit")
    info["total_true"].append(nhit)
    hit_ids = e_data.GetAttr("fSiPMHitID")
    # minus dead sipm
    adj_hit = 0
    hit_ids_counter = Counter(hit_ids)
    for d_sipm,d_adj in zip(dead_list,adjs):
        dead_hit = hit_ids_counter[d_sipm]
        nhit -= dead_hit
        info[d_sipm]["true"].append(dead_hit)
        adj_hits = []
        for j in d_adj:
            adj_hits.append(hit_ids_counter[j])
        adj_hit += np.mean(adj_hits)
        info[d_sipm]["pred"].append(np.mean(adj_hits))
    info["total_unc"].append(nhit)
    info["total_pred"].append(nhit + adj_hit)


fig = plt.figure()
bin_range = [np.mean(info["total_true"])*0.86,np.max(info["total_pred"])*1.01]
plt.hist(info["total_true"],histtype="step",linewidth=2,
        label="True hit\n(mean: %.1f)"%(np.mean(info["total_true"])),bins=30,range=bin_range)
plt.hist(info["total_pred"],histtype="step",linewidth=2,
        label="Correct dead readout\n(mean: %.1f)"%(np.mean(info["total_pred"])),bins=30,range = bin_range)
plt.hist(info["total_unc"],histtype="step",linewidth=2,
        label="Uncorrect dead readout\n(mean: %.1f)"%(np.mean(info["total_unc"])),bins=30,range = bin_range)
plt.legend(loc = "upper left")
plt.xlabel("R [mm]",fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("$\\theta [\circ]$",fontsize=16)
plt.tight_layout()
output = "../result/nonuniformity/fig/average_correct_for_dead_readout_spectrum.eps"
plt.savefig(output)
print("Fig save to %s"%(output))
plt.show()

# plot correct for every channel
hit_bias = []
for d_sipm in dead_list:
    bias = (np.mean(info[d_sipm]["true"]) - np.mean(info[d_sipm]["pred"]))/np.mean(info[d_sipm]["true"])
    hit_bias.append(bias)
plt.plot(hit_bias,linewidth=2)
plt.xlabel("Dead channels index",fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("$(Hit_{true} - Hit_{cor})/Hit_{true}$ [%]",fontsize=16)
plt.tight_layout()
output = "../result/nonuniformity/fig/average_correct_for_dead_readout_hitbias.eps"
plt.savefig(output)
print("Fig save to %s"%(output))
plt.show()
