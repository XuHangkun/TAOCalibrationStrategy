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
    for event in tqdm(events):
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
        "../result/nonuniformity/uniform_IBD_reconstructed_by_ideal_numap.pkl",
        "../result/nonuniformity/IBD_reconstructed_by_calib_numap.pkl",
        "../result/nonuniformity/IBD_reconstructed_by_calib_numap_vertexsmear.pkl",
                ])
    parser.add_argument('--uniform_labels', nargs="+" ,default = [
        "Calib. by $g_{ideal}$","Calib. by $g_{\gamma}$","Add vertex smear"
        ])
    parser.add_argument('--central_input', default = "../result/nonuniformity/central_IBD_reconstructed_by_ideal_numap.pkl")
    parser.add_argument('--output_resolution', default = "../result/nonuniformity/fig/IBD_reconstructed_resolution.eps")
    parser.add_argument('--output_bias', default = "../result/nonuniformity/fig/IBD_reconstructed_bias.eps")
    parser.add_argument('--kinetic', default = 3, type = int)
    args = parser.parse_args()
    print(args)

    energies = range(0,9)
    info = {
            }
    for r_file,label in zip(args.uniform_inputs,args.uniform_labels):
        f = open(r_file,"rb")
        uniform_events = pickle.load(f)
        f.close()
        info[label] = {"mean":[],"std":[]}
        for e in energies:
            corrected_hits = extract_info(uniform_events,ki = e)
            info[label]["mean"].append(np.mean(corrected_hits))
            info[label]["std"].append(100*np.std(corrected_hits)/np.mean(corrected_hits))

    central_info = {"mean":[],"std":[]}
    f = open(args.central_input,"rb")
    central_events = pickle.load(f)
    f.close()
    for e in energies:
        corrected_hits = extract_info(central_events,ki = e,mode="u")
        central_info["mean"].append(np.mean(corrected_hits))
        central_info["std"].append(100*np.std(corrected_hits)/np.mean(corrected_hits))

    # plot standard deviation
    fig = plt.figure()
    gs0 = gridspec.GridSpec(2, 1, height_ratios=[3, 1],hspace=0.0)
    plt.subplot(gs0[0])
    plt.plot(energies,central_info["std"],marker="o",label="central")
    for label in args.uniform_labels:
        plt.plot(energies,info[label]["std"],marker="o",label=label)
    plt.legend(loc = "upper right",fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel("$\\frac{\sigma}{E}$ [%]",fontsize=16)
    plt.grid(axis="y")
    # plt.ylim(0.55,2.0)

    plt.subplot(gs0[1])
    v = np.power(np.array(info[args.uniform_labels[0]]["std"]),2) - np.power(np.array(central_info["std"]),2)
    plt.plot(energies,np.power(np.power(v,2),1./4))
    for label in args.uniform_labels:
        v = np.power(np.array(info[label]["std"]),2) - np.power(np.array(central_info["std"]),2)
        plt.plot(energies,np.power(np.power(v,2),1./4),marker="o")
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
    v = 100*(np.array(info[args.uniform_labels[0]]["mean"]) - np.array(central_info["mean"]))/np.array(central_info["mean"])
    plt.plot(energies,v,marker="o")
    for label in args.uniform_labels:
        v = 100*(np.array(info[label]["mean"]) - np.array(central_info["mean"]))/np.array(central_info["mean"])
        plt.plot(energies,v,marker="o",label=label)
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
