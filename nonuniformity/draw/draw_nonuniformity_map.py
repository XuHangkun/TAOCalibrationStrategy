import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from utils import TaoNuMap
import argparse
import pickle
from utils import config
from mpl_toolkits.axes_grid1 import make_axes_locatable


def draw_nonuniformity_map():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input',default = config["idealmap_path"])
    parser.add_argument('--kind',default = "linear",choices=["linear","cubic"])
    parser.add_argument('--output',default = "../result/nonuniformity/fig/ideal_nonuniformity_map.eps")
    args = parser.parse_args()
    print(args)

    file = open(args.input,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind=args.kind)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(0, 850, 10)
    Y = np.arange(0, 180, 3)
    X, Y = np.meshgrid(X, Y)
    Z = tao_nu_map(X,Y)

    # Plot the surface.
    # make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # ax.scatter(tao_nu_map.radius,tao_nu_map.theta,tao_nu_map.value)

    # Customize the z axis.
    ax.set_zlim(0.7, 1.05)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    fig.colorbar(surf, fraction = 0.046,pad = 0.04,shrink = 0.6)
    ax.set_xlabel("R [mm]",fontsize=14)
    ax.set_ylabel("$\\theta [\circ]$",fontsize=14)
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel("$g_{ideal}(r,\\theta)$",rotation=90,fontsize=14)
    ax.zaxis._axinfo['juggled'] = (1,2,0)
    plt.savefig(args.output)
    print("Save fig to %s"%(args.output))

    plt.show()

if __name__ == "__main__":
    draw_nonuniformity_map()
