from nonuniformity.draw.draw_numap_byanchor import draw_chi2_map
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from utils import TaoNuMap
import argparse
import pickle
from utils import config,create_numap_byidealline,AnchorOptimizer

def draw_map_diff(agrs):

    file = open(args.first_numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map_1 = TaoNuMap(mapinfo,kind="linear")

    file = open(args.second_numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map_2 = TaoNuMap(mapinfo)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(0, 700, 10)
    Y = np.arange(0, 180, 3)
    X, Y = np.meshgrid(X, Y)
    Z = tao_nu_map_1(X,Y) - tao_nu_map_2(X,Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    # ax.set_zlim(0.6, 1.05)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.03f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--first_numap_path',default = config["idealmap_path"])
    parser.add_argument('--second_numap_path',default = "../result/nonuniformity/ideal_point_calib_info.pkl")
    args = parser.parse_args()
    print(args)
    draw_map_diff(args)
    