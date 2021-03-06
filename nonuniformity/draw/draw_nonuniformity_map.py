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
    parser.add_argument('--input',default = config["idealmap_path"])
    parser.add_argument('--kind',default = "linear",choices=["linear","cubic"])
    parser.add_argument('--calib_point',action="store_true")
    parser.add_argument('--output',default = "../result/nonuniformity/fig/ideal_nonuniformity_map.eps")
    args = parser.parse_args()
    print(args)

    file = open(args.input,"rb")
    mapinfo = pickle.load(file)
    # we should add a filter here.
    filtered_mapinfo = []
    for item in mapinfo:
        if gamma_fitable(item["r"],item["theta"]):
            filtered_mapinfo.append(item)
    tao_nu_map = TaoNuMap(filtered_mapinfo,kind=args.kind)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(1.e-1, 850, 10)
    Y = np.arange(1.e-1, 179.9, 3)
    X, Y = np.meshgrid(X, Y)
    Z = tao_nu_map(X,Y)
    # X = []
    # Y = []
    # for i in np.arange(1.e-1,850,10):
    #     for j in np.arange(1.e-1,179.9,3):
    #         if gamma_fitable(i,j):
    #             X.append(i)
    #             Y.append(j)
    # Z = tao_nu_map(np.array(X),np.array(Y))

    # Plot the surface.
    # make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    surf = ax.plot_surface(X, Y, Z, cmap = cm.coolwarm ,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(0.7, 1.05)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    cbar =  fig.colorbar(surf,
            ax = ax,
            fraction = 0.046,
            pad = 0.04,shrink = 0.6,
            format = "%.2f"
            )

    # plot calibration point
    true_calib_point = {"r":[],"theta":[],"value":[]}
    false_calib_point = {"r":[],"theta":[],"value":[]}
    for item in mapinfo:
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
        ax.scatter(true_calib_point["r"],true_calib_point["theta"],true_calib_point["value"],label="True Calib. Point",color="blue")
        ax.scatter(false_calib_point["r"],false_calib_point["theta"],false_calib_point["value"],label="Symmetry Calib. Point",color="green")

    cbar.ax.tick_params(labelsize=14)
    ax.set_xlabel("R [mm]",fontsize=16)
    ax.set_ylabel("$\\theta [\circ]$",fontsize=16)
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel("$g(r,\\theta)$",rotation=90,fontsize=16)
    ax.zaxis._axinfo['juggled'] = (1,2,0)
    plt.xticks(fontsize=14)
    plt.yticks([0,30,60,90,120,150,180],fontsize=14)
    ax.set_zticks([0.75,0.85,0.95,1.05])
    plt.legend(frameon=False)
    # change fontsize
    for t in ax.zaxis.get_major_ticks(): t.label.set_fontsize(14)
    plt.tight_layout()
    plt.savefig(args.output)
    print("Save fig to %s"%(args.output))
    plt.show()

if __name__ == "__main__":
    draw_nonuniformity_map()
