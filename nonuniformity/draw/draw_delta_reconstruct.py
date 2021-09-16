import argparse
import pandas as pd
import pickle
from utils import approx_equal
# import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from tqdm import tqdm
from utils import config
import numpy as np
from matplotlib import gridspec

def extract_info(events,ki = 1,mode="c"):
    corrected_hits = []
    uniform_hits = []
    for event in events:
        kinetic = event["prim_particle_ke"]
        if not approx_equal(kinetic,ki):
            continue
        edep = event["edep"]
        if not approx_equal(edep,ki + 1.022):
            continue
        corrected_hit = event["corrected_nhit"]
        nhit = event["nhit"]
        corrected_hits.append(corrected_hit/config["energy_scale"])
        uniform_hits.append(nhit/config["energy_scale"])
    if mode == "u":
        return uniform_hits
    else:
        return corrected_hits

def draw():
    parser = argparse.ArgumentParser()
    parser.add_argument('--uniform_inputs', nargs="+" ,default = [
        "../result/nonuniformity/map/IBD_uniform_reconstructed_by_calib_numap_sipmdead_seed%d.pkl"%(i) for i in range(20)
                ])
    parser.add_argument('--central_input', nargs = "+",default = [
        "../result/nonuniformity/map/IBD_central_reconstructed_by_calib_numap_sipmdead_seed%d.pkl"%(i) for i in range(20)
        ]
    )
    parser.add_argument('--output_resolution', default = "../result/nonuniformity/fig/IBD_reconstructed_resolution.eps")
    parser.add_argument('--output_bias', default = "../result/nonuniformity/fig/IBD_reconstructed_bias.eps")
    parser.add_argument('--kinetic', default = 3, type = int)
    parser.add_argument('--num', default = 20, type = int)
    args = parser.parse_args()
    print(args)

    energies = range(0,9)
    info = {
            }
    num = 0
    for r_uni_file,r_cen_file,label in tqdm(zip(args.uniform_inputs,args.central_input,range(len(args.central_input)))):
        f = open(r_uni_file,"rb")
        uniform_events = pickle.load(f)
        f.close()
        f = open(r_cen_file,"rb")
        central_events = pickle.load(f)
        f.close()
        info[label] = {"mean":[],"std":[]}
        for e in energies:
            corrected_uni_hits = extract_info(uniform_events,ki = e)
            corrected_cen_hits = extract_info(central_events,ki = e,mode="u")
            mean_bias = 100*(np.mean(corrected_uni_hits) - np.mean(corrected_cen_hits))/np.mean(corrected_cen_hits)
            std_inc = np.power(np.std(corrected_uni_hits)/np.mean(corrected_uni_hits),2) - np.power(np.std(corrected_cen_hits)/np.mean(corrected_cen_hits),2)
            info[label]["mean"].append(mean_bias)
            info[label]["std"].append(100*np.power(np.power(std_inc,2),1./4))
        num += 1
        if num > args.num:
            break

    # plot standard deviation
    fig = plt.figure()
    for label in info.keys():
        plt.plot(energies,info[label]["std"])
    plt.yticks(fontsize=14)
    # plt.ylim(0,0.5)
    plt.ylabel("$\\frac{\sqrt{|\sigma_{rec}^{2} - \sigma_{central}^{2}|}}{E}$ [%]",fontsize=16)
    plt.xlabel("$e^{+}$ kinetic [MeV]",fontsize=16)
    plt.xticks(fontsize=14)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(args.output_resolution)
    print("Fig save to %s"%(args.output_resolution))
    plt.show()

    # plot bias
    fig = plt.figure()
    for label in info.keys():
        plt.plot(energies,info[label]["mean"])
    plt.yticks(fontsize=14)
    plt.ylabel("$\\frac{E_{vis}^{rec} - E_{vis}^{central}}{E_{vis}^{central}}$ [%]",fontsize=16)
    plt.xlabel("$e^{+}$ kinetic [MeV]",fontsize=16)
    plt.xticks(fontsize=14)
    plt.grid(axis="y")
    plt.legend(fontsize=14)
    # plt.ylim(0,0.3)
    plt.tight_layout()
    plt.savefig(args.output_bias)
    print("Fig save to %s"%(args.output_bias))
    plt.show()

if __name__ == "__main__":
    draw()
