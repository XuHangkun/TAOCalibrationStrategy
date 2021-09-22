import matplotlib.pyplot as plt
from nonlin_model import GammaNL
from utils import config,read_pickle_data
import argparse
import numpy as np
from matplotlib import gridspec

def read_gamma_info(info,source,key):
    l = []
    for s in source:
        l.append(info[s][key])
    return l

def draw_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gamma_best_fit_pars',
            default = "../result/nonlinearity/fit/fit_gamma_best_pars.pkl")
    parser.add_argument('--total_best_fit_pars',
            default = "../result/nonlinearity/fit/fit_total_best_pars.pkl")
    parser.add_argument('--output',
            default = "../result/nonlinearity/fig/gamma_fitting.eps")
    args = parser.parse_args()
    print(args)
    return args

def draw_gamma_nonlin(args):
    # gamma nonlinearity
    gamma_nonlin = GammaNL()
    gamma_best_fit = read_pickle_data(args.gamma_best_fit_pars)[0]
    total_best_fit = read_pickle_data(args.total_best_fit_pars)[0]
    gamma_source = ["Ge68","Cs137","Mn54","Co60","K40","nH","O16"]
    radioactive_info = config["radioactive_source"]
    e_true = read_gamma_info(radioactive_info,gamma_source,"energy")
    labels = read_gamma_info(radioactive_info,gamma_source,"label")
    gamma_num = read_gamma_info(radioactive_info,gamma_source,"gamma_num")
    e_vis = read_gamma_info(gamma_best_fit["gamma_info"],gamma_source,"e_vis")
    e_vis = np.array(e_vis)/np.array(e_true)
    uncertainty = read_gamma_info(gamma_best_fit["gamma_info"],gamma_source,"uncertainty")
    uncertainty = np.array(uncertainty)/np.array(e_true)
    e_true = np.array(e_true)/np.array(gamma_num)

    # best pars
    gamma_fit_pars_value = gamma_best_fit["pars"]
    total_fit_pars_value = total_best_fit["pars"]
    pred_nonlin_gamma = np.array([gamma_nonlin(key,*gamma_fit_pars_value) for key in gamma_source])
    pred_nonlin_total = np.array([gamma_nonlin(key,*total_fit_pars_value) for key in gamma_source])

    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1],hspace=0.0)
    plt.subplot(gs[0])
    # Draw gamma data
    plt.errorbar(e_true,e_vis,uncertainty,fmt="o",label="data")
    plt.errorbar(e_true-0.1,pred_nonlin_gamma,fmt="o",label="Best fit without $^{12}B$ constraint")
    plt.errorbar(e_true+0.1,pred_nonlin_total,fmt="o",label="Best fit with $^{12}B$ constraint")
    # plot text here
    for et,ev,label in zip(e_true,e_vis,labels):
        plt.text(et + 0.2,ev,label,verticalalignment = "center",fontsize=12)
    plt.ylabel("$E_{vis}/E^{\gamma}$",fontsize=16)
    plt.ylim(0.901,1.042)
    plt.xlim(0.2,6.9)
    plt.yticks(fontsize=14)
    plt.grid(axis="y")
    plt.legend(fontsize=12)
    plt.subplot(gs[1])
    plt.errorbar(e_true,100*(pred_nonlin_gamma - e_vis)/e_vis,fmt="o",label="Best fit without $^{12}B$ constraint")
    plt.errorbar(e_true,100*(pred_nonlin_gamma - e_vis)/e_vis,fmt="o",label="Best fit without $^{12}B$ constraint")
    plt.errorbar(e_true,100*(pred_nonlin_total - e_vis)/e_vis,fmt="o",label="Best fit with $^{12}B$ constraint")
    plt.xlabel("$E^{\gamma}$ [MeV]",fontsize=16)
    plt.ylabel("Bias [%]",fontsize=16)
    plt.ylim(-0.25,0.25)
    plt.xlim(0.2,6.9)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(args.output)
    print("Fig save to %s"%(args.output))
    plt.show()

if __name__ == "__main__":
    args = draw_args()
    draw_gamma_nonlin(args)
