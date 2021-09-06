import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from utils import TaoNuMap
import argparse
import pickle
from utils import config
from mpl_toolkits.axes_grid1 import make_axes_locatable
from utils import gamma_fitable

def draw_nonuniformity_map():

    parser = argparse.ArgumentParser()
    parser.add_argument('--ideal_map',default = config["idealmap_path"])
    parser.add_argument('--calib_map',default = "../result/nonuniformity/point_calib_map.pkl")
    parser.add_argument('--kind',default = "cubic",choices=["linear","cubic"])
    parser.add_argument('--calib_point',action="store_true")
    parser.add_argument('--output',default = "../result/nonuniformity/fig/ideal_calib_map_diff.eps")
    args = parser.parse_args()
    print(args)

    file = open(args.ideal_map,"rb")
    idealmapinfo = pickle.load(file)
    tao_ideal_map = TaoNuMap(idealmapinfo,kind=args.kind)

    file = open(args.calib_map,"rb")
    calibmapinfo = pickle.load(file)
    # we should add a filter here.
    filtered_calibmapinfo = []
    for item in calibmapinfo:
        if gamma_fitable(item["r"],item["theta"]):
            filtered_calibmapinfo.append(item)
    tao_calib_map = TaoNuMap(filtered_calibmapinfo,kind=args.kind)

    fig, ax = plt.subplots()

    # Make data.
    X = np.arange(0, 860, 10)
    Y = np.arange(0, 183, 3)
    X, Y = np.meshgrid(X, Y)
    Z = tao_calib_map(X,Y) - tao_ideal_map(X,Y)
    print(np.max(Z[X<650]),np.min(Z[X < 650]))

    # Plot the surface.
    # make the panes transparent
    surf = plt.pcolormesh(X, Y, Z, shading='auto')

    # Add a color bar which maps values to colors.
    cbar =  fig.colorbar(surf,
            ax = ax,
            fraction = 0.046,
            pad = 0.04,
            format = "%.2f"
            )

    # plot calibration point
    true_calib_point = {"r":[],"theta":[],"value":[]}
    false_calib_point = {"r":[],"theta":[],"value":[]}
    for item in calibmapinfo:
        #if not item["nu_value"]:
        #    continue
        print(item["r"],item["theta"],item["realistic"],item["nu_value"])
        if not gamma_fitable(item["r"],item["theta"]):
            continue
        if not item["realistic"] and item["r"] > 1:
            false_calib_point["r"].append(item["r"])
            false_calib_point["theta"].append(item["theta"])
            false_calib_point["value"].append(item["nu_value"])
        else:
            true_calib_point["r"].append(item["r"])
            true_calib_point["theta"].append(item["theta"])
            true_calib_point["value"].append(item["nu_value"])
    if args.calib_point:
        ax.scatter(true_calib_point["r"],true_calib_point["theta"],
                label="Calib. Point",color="blue")
        ax.scatter(false_calib_point["r"],false_calib_point["theta"],label="Symmetry Point",
                color="",marker='o',edgecolors='blue')
    ax.grid(False)
    plt.plot([650,650],[0,180],linestyle="dotted",color="red",linewidth=5)
    cbar.ax.tick_params(labelsize=14)
    ax.set_xlabel("R [mm]",fontsize=16)
    ax.set_ylabel("$\\theta [\circ]$",fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks([0,30,60,90,120,150,180],fontsize=14)
    plt.legend(frameon=False,fontsize=12)
    plt.tight_layout()
    plt.xlim(0,np.max(true_calib_point["r"]))
    plt.ylim(0,180)
    plt.savefig(args.output)
    print("Save fig to %s"%(args.output))
    plt.show()

if __name__ == "__main__":
    draw_nonuniformity_map()
