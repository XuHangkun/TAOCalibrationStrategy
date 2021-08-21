import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from utils import TaoNuMap
import argparse
import pickle
from utils import config,create_numap_byidealline,AnchorOptimizer

def draw_chi2_map(args):
    file = open(args.ideal_numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind="linear")
    optimizer = AnchorOptimizer(tao_nu_map)
    first_theta = np.arange(args.anchor_pars[0] - 2.5, args.anchor_pars[0] + 2.5, 0.5)
    second_theta = np.arange(args.anchor_pars[1] - 2.5, args.anchor_pars[1] + 2.5, 0.5)
    first_theta, second_theta = np.meshgrid(first_theta, second_theta)
    chi2 = np.ones(first_theta.shape)
    for i in range(chi2.shape[0]):
        for j in range(chi2.shape[1]):
            # anchors define
            first_anchor = {"r":900,"theta":first_theta[i][j],"phi":0}
            second_anchor = {"r":900,"theta":second_theta[i][j],"phi":args.anchor_pars[2]}
            chi2[i][j] = optimizer(first_anchor,second_anchor)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Plot the surface.
    surf = ax.plot_surface(first_theta, second_theta, chi2, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    # ax.set_zlim(0.6, 1.05)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.03f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def draw_nonuniformity_map(agrs):

    file = open(args.ideal_numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind="linear")

    # anchors define
    first_anchor = {"r":900,"theta":args.anchor_pars[0],"phi":0}
    second_anchor = {"r":900,"theta":args.anchor_pars[1],"phi":args.anchor_pars[2]}
    anchor_line_numap = create_numap_byidealline(
        tao_nu_map,
        first_anchor=first_anchor,
        second_anchor=second_anchor
    )

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(0, 700, 10)
    Y = np.arange(0, 180, 3)
    X, Y = np.meshgrid(X, Y)
    Z = anchor_line_numap(X,Y) - tao_nu_map(X,Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # ax.scatter(anchor_line_numap.radius,anchor_line_numap.theta,anchor_line_numap.value)

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
    parser.add_argument('--ideal_numap_path',default = config["idealmap_path"])
    parser.add_argument('--anchor_pars',default = [102.4900762,155.22267625,151.73342866])
    # parser.add_argument('--anchor_pars',default = [104.14737545,149.83746501,151.70991139])
    args = parser.parse_args()
    print(args)
    # draw_nonuniformity_map(args)
    draw_chi2_map(args)
