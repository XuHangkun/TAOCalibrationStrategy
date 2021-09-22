from nonlin_model import ElectronNL
import numpy as np
import matplotlib.pyplot as plt
import argparse
from matplotlib import gridspec
from utils import config,read_pickle_data
from scipy import interpolate
import os

def cal_sigma_band(files,x):
    total_data = []
    ele_nonlin = ElectronNL()
    for f in files:
        datas = read_pickle_data(f)
        for data in datas:
            pars = data["pars"]
            total_data.append(ele_nonlin(x,*pars))
    total_data = np.array(total_data)
    return np.min(total_data,axis=0), np.max(total_data,axis=0)

def generate_files(file_pattern,file_num):
    return [file_pattern%(i) for i in range(file_num) if os.path.exists(file_pattern%(i))]

def draw_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gamma_best_fit_pars',
            default = "../result/nonlinearity/old_fit/fit_total_best_pars.pkl")
            # default = "../result/nonlinearity/old_fit/fit_gamma_best_pars.pkl")
    parser.add_argument('--gamma_sigma_fit_pars',
            default = "../result/nonlinearity/old_fit/fit_total_nonlin_sigmaband_v%d.pkl")
            # default = "../result/nonlinearity/old_fit/fit_gamma_nonlin_sigmaband_v%d.pkl")
    parser.add_argument('--total_best_fit_pars',
            default = "../result/nonlinearity/old_fit/fit_total_best_pars.pkl")
    parser.add_argument('--total_sigma_fit_pars',
            default = "../result/nonlinearity/fit/fit_total_nonlin_sigmaband_v%d.pkl")
    parser.add_argument('--file_num',default=200,type=int)
    parser.add_argument('--output',
            default = "../result/nonlinearity/fig/electron_nonlin.pdf")
    args = parser.parse_args()
    print(args)
    return args

def draw_electron_nonlin(args):
    x = np.arange(0.5,8.1,0.1)
    ele_nonlin = ElectronNL()
    # load true electron non-linearity
    true_electron_nonlin_info = read_pickle_data(config["true_electron_nonlin_file"])
    true_electron_nonlin_func = interpolate.interp1d(
            true_electron_nonlin_info["edep"],true_electron_nonlin_info["ratio"])
    true_electron_nonlin = true_electron_nonlin_func(x)
    # load gamma best best fit and sigma band
    gamma_best_fit = read_pickle_data(args.gamma_best_fit_pars)[0]
    gamma_best_ele_nonlin = ele_nonlin(x,*gamma_best_fit["pars"])
    fs = generate_files(args.gamma_sigma_fit_pars,args.file_num)
    gamma_down_ele_nonlin,gamma_up_ele_nonlin = cal_sigma_band(fs,x)
    # load total best best fit and sigma band
    total_best_fit = read_pickle_data(args.total_best_fit_pars)[0]
    total_best_ele_nonlin = ele_nonlin(x,*total_best_fit["pars"])
    fs = generate_files(args.total_sigma_fit_pars,args.file_num)
    total_down_ele_nonlin,total_up_ele_nonlin = cal_sigma_band(fs,x)

    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1],hspace=0.0)
    plt.subplot(gs[0])
    gamma_color = "green"
    total_color = "red"
    plt.plot(x,true_electron_nonlin,color="black",linewidth=2,label="Inherent nonlinearity")
    plt.plot(x,gamma_best_ele_nonlin,linewidth=2,color = gamma_color,label="Best fit without $^{12}B$ constraint")
    plt.fill_between(x,gamma_down_ele_nonlin,gamma_up_ele_nonlin,alpha=0.4,label="68% C.L. without $^{12}B$ constraint",color=gamma_color)
    plt.plot(x,total_best_ele_nonlin,linewidth=2,color = total_color,label="Best fit with $^{12}B$ constraint")
    plt.fill_between(x,total_down_ele_nonlin,total_up_ele_nonlin,alpha=0.4,label="68% C.L. with $^{12}B$ constraint",color=total_color)
    plt.ylabel("$E_{vis}/E^{e}$",fontsize=16)
    plt.ylim(0.961,1.08)
    plt.yticks(fontsize=14)
    plt.grid(axis="y")
    plt.legend(fontsize=12)
    plt.subplot(gs[1])
    plt.plot(x,100*(gamma_best_ele_nonlin - true_electron_nonlin)/true_electron_nonlin,linewidth=2,color = gamma_color)
    plt.fill_between(x,
            100*(gamma_down_ele_nonlin - true_electron_nonlin)/true_electron_nonlin,
            100*(gamma_up_ele_nonlin - true_electron_nonlin)/true_electron_nonlin,
            alpha=0.4,label="68% C.L. without $^{12}B$ constraint",color=gamma_color)
    plt.plot(x,100*(total_best_ele_nonlin - true_electron_nonlin)/true_electron_nonlin,linewidth=2,color = total_color)
    plt.fill_between(x,
            100*(total_down_ele_nonlin - true_electron_nonlin)/true_electron_nonlin,
            100*(total_up_ele_nonlin - true_electron_nonlin)/true_electron_nonlin,
            alpha=0.4,label="68% C.L. without $^{12}B$ constraint",color=total_color)
    plt.xlabel("$E^{e}$ [MeV]",fontsize=16)
    plt.ylabel("Bias [%]",fontsize=16)
    plt.ylim(-1.2,1.2)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(args.output)
    print("Fig save to %s"%(args.output))
    plt.show()

if __name__ == "__main__":
    args = draw_args()
    draw_electron_nonlin(args)

