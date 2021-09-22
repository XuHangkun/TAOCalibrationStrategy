import matplotlib.pyplot as plt
from nonlin_model import ContinuousSpecNL
from utils import config,read_pickle_data,rhist2np
import argparse
import numpy as np
from matplotlib import gridspec
from preprocess import ContinuousSpecDataset

def read_gamma_info(info,source,key):
    l = []
    for s in source:
        l.append(info[s][key])
    return l

def draw_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--total_best_fit_pars',
            default = "../result/nonlinearity/fit/fit_total_best_pars.pkl")
    parser.add_argument('--output',
            default = "../result/nonlinearity/fig/b12_fitting.eps")
    args = parser.parse_args()
    print(args)
    return args

def smooth_line(x,y,num=2):
    for i in range(num,len(y)-num):
        y[i] = np.mean([y[i + k] for k in range(-num,num+1)])
    return x,y

def draw_continuous_nonlin(args):
    # continuous nonlinearity
    cspec_dataset = ContinuousSpecDataset()
    cspec_evis,cspec_edep = cspec_dataset.get_data()
    cspec_nonlin = ContinuousSpecNL(cspec_edep)

    # best pars
    total_best_fit = read_pickle_data(args.total_best_fit_pars)[0]
    total_fit_pars_value = total_best_fit["pars"]
    pred_hist = cspec_nonlin(*total_fit_pars_value)

    fig = plt.figure()
    # Draw gamma data
    cspec_evis_x,cspec_evis_y = rhist2np(cspec_evis)
    plt.step(cspec_evis_x,cspec_evis_y,label="Data",linewidth=2)
    pred_evis_x,pred_evis_y = rhist2np(pred_hist)
    pred_evis_x,pred_evis_y = smooth_line(pred_evis_x,pred_evis_y)
    plt.plot(pred_evis_x[30:121],pred_evis_y[30:121],label="Best fit with $^{12}B$ constraint",linewidth=2)
    plt.ylabel("$A.U.$",fontsize=16)
    plt.yticks(fontsize=14)
    plt.xlabel("$E_{vis}$ of $^{12}B$ [MeV]",fontsize=16)
    plt.xticks(fontsize=14)
    plt.grid(axis="y")
    plt.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig(args.output)
    print("Fig save to %s"%(args.output))
    plt.show()

if __name__ == "__main__":
    args = draw_args()
    draw_continuous_nonlin(args)
