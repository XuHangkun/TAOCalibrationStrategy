from utils import config
from utils import SimpleNHMCShape,read_gamma_hit
from utils import read_yaml_data, save_yaml_data
from TaoDataAPI import TAOData
import pandas as pd
import numpy as np
import ROOT
import time
import matplotlib.pyplot as plt
from utils import rhist2np

def fit_nH(
        name = "nH",
        config_file = "./input/fit/ra_fit_info.yaml",
        update_config_file = False
        ):
    # Read config file
    config_data = read_yaml_data(config_file)
    # load data
    ra_info = config_data[name]
    files = [ra_info["file_path"]]
    h_hit, h_full_hit = read_gamma_hit(
            source = name,
            files = files,
            energy = 2.22569,             # n-H energy
            num = 72000
            )
    # define TF1
    mcshape = SimpleNHMCShape()
    A = ROOT.TF1("tmp",mcshape,0,1.1*2.22,5)
    pars = [2e4,2.2,2.2*0.015,2e2,10]
    for i in range(5):
        A.SetParameter(i,pars[i])
    A.SetNpx(500)

    # Fit
    fit_lim = (1.6,2.5)
    result = h_hit.Fit("tmp","S","",fit_lim[0], fit_lim[1])
    chi2 = result.Chi2()
    ndf = result.Ndf()
    pars = [h_hit.GetFunction("tmp").GetParameter(i) for i in range(5)]
    pars_error = [h_hit.GetFunction("tmp").GetParError(i) for i in range(5)]
    bias = 100*(pars[1] - h_full_hit.GetMean())/h_full_hit.GetMean()
    bias_error = 100*np.sqrt(pars_error[1]**2 + h_full_hit.GetMeanError()**2)/h_full_hit.GetMean()
    print(f"%s : bias = {bias:.4f}, bias error = {bias_error:.4f}"%(name))
    bias_info = {"fit_bias":bias,"uncertainty":bias_error,"nPE":h_full_hit.GetMean()}
    # update config file!
    if update_config_file:
        for k,v in bias_info.items():
            config_data[name][k] = v
        print("Update fit_bias, uncertainty, nPE in %s"%(config_file))
        save_yaml_data(config_data, config_file)

    # plot fig
    h_x,h_y = rhist2np(h_hit)
    h_x_s = h_x[(h_x > fit_lim[0]) & (h_x < fit_lim[1])]
    h_y = h_y[(h_x > fit_lim[0]) & (h_x < fit_lim[1])]
    h_x = h_x[(h_x > fit_lim[0]) & (h_x < fit_lim[1])]
    eleak_y = [mcshape.leak_energy_spec([x],pars) for x in h_x_s]
    total_y = [mcshape([x],pars) for x in h_x_s]
    fig = plt.figure()
    plt.errorbar(h_x,h_y,np.sqrt(h_y),linewidth=1,ms=2,fmt="o",label="Simulated data")
    plt.plot(h_x_s,total_y,label="Best fit")
    plt.plot(h_x_s,eleak_y,"--",label="Energy leak")
    plt.legend()
    plt.xlabel("$E_{vis}$ [MeV]",fontsize=16)
    plt.ylabel("Count",fontsize=16)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.tight_layout()
    fig_path = "../result/nonlinearity/fig/%s_spec_fit.eps"%(name)
    plt.savefig(fig_path)
    print("Fig save to %s"%(fig_path))
    plt.show()

    return bias_info

if __name__ == "__main__":
    fit_nH()
