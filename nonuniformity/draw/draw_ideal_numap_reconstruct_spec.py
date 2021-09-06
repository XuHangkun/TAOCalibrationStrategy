import argparse
import pandas as pd
import pickle
from utils import approx_equal
# import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from tqdm import tqdm
from utils import config

def draw():
    parser = argparse.ArgumentParser()
    parser.add_argument('--uniform_input', default = "../result/nonuniformity/uniform_IBD_reconstructed_by_ideal_numap.pkl")
    parser.add_argument('--central_input', default = "../result/nonuniformity/central_IBD_reconstructed_by_ideal_numap.pkl")
    parser.add_argument('--output', default = "../result/nonuniformity/fig/IBD_spec_reconstructed_by_ideal_numap.eps")
    parser.add_argument('--kinetic', default = 3, type = int)
    args = parser.parse_args()
    print(args)

    f = open(args.uniform_input,"rb")
    uniform_events = pickle.load(f)
    f.close()
    f = open(args.central_input,"rb")
    central_events = pickle.load(f)
    f.close()

    corrected_hits = []
    uniform_hits = []
    for event in tqdm(uniform_events):
        kinetic = event["prim_particle_ke"]
        if not approx_equal(kinetic,args.kinetic):
            continue
        edep = event["edep"]
        if not approx_equal(edep,args.kinetic + 1.022):
            continue
        corrected_hit = event["corrected_nhit"]
        nhit = event["nhit"]
        corrected_hits.append(corrected_hit/config["energy_scale"])
        uniform_hits.append(nhit/config["energy_scale"])
    
    central_hits = []
    for event in tqdm(central_events):
        kinetic = event["prim_particle_ke"]
        if not approx_equal(kinetic,args.kinetic):
            continue
        edep = event["edep"]
        if not approx_equal(edep,args.kinetic + 1.022):
            continue
        nhit = event["nhit"]
        central_hits.append(nhit/config["energy_scale"])
    
    fig = plt.figure()
    plt.hist(central_hits, bins=100, label="central",histtype="step",density=True)
    plt.hist(uniform_hits, bins=100, label="uniform distributed",histtype="step",density=True)
    plt.hist(corrected_hits,color="red",bins=100, label="corrected",histtype="step",density=True)
    plt.legend(loc = "upper left")
    plt.xlabel("$E_{vis}^{prompt}$ [MeV]",fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel("A.U.",fontsize=16)
    plt.tight_layout()
    plt.savefig(args.output)
    print("Fig save to %s"%(args.output))
    plt.show()

if __name__ == "__main__":
    draw()