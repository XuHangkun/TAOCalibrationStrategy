import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from utils import TaoNuMap
import argparse
import pickle
from utils import config


def draw_nonuniformity_map():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',default = config["idealmap_path"])
    args = parser.parse_args()
    print(args)

    file = open(args.input,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind="linear")

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(0, 850, 10)
    Y = np.arange(0, 180, 3)
    X, Y = np.meshgrid(X, Y)
    Z = tao_nu_map(X,Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(0.6, 1.05)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

if __name__ == "__main__":
    draw_nonuniformity_map()