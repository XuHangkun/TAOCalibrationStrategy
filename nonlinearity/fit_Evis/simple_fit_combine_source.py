from utils import config
from utils import MulSimpleMCShape, SimpleMCShape, read_gamma_hit
from utils import read_yaml_data, save_yaml_data
from TaoDataAPI import TAOData
import pandas as pd
import numpy as np
import ROOT
import time
import matplotlib.pyplot as plt
from utils import rhist2np

def fit_combinesource(
        config_file = "./input/fit/ra_fit_info.yaml",
        update_config_file = False
        ):
    # Read config file
    config_data = read_yaml_data(config_file)

    # get energy scale
    nake_true_info = "./input/fit/nake_true_info.yaml"
    nake_true_info = read_yaml_data(nake_true_info)
    energy_scale = nake_true_info["nH"]["nake_evis"]/nake_true_info["nH"]["mean_gamma_e"]

    # load data
    sources = ["Cs137","Mn54","K40","Co60"]
    energies = []
    labels = []
    hists = []
    full_hists = []
    for source in sources:
        source_info = config_data[source]
        energies.append(source_info["total_gamma_e"])
        labels.append(source_info["label"])
        files = [source_info["file_path"]]
        h_hit,h_full_hit = read_gamma_hit(
                source = source,
                files = files,
                energy = source_info["total_gamma_e"],
                energy_scale = energy_scale,
                xrange = [0.1,3.0],
                num = source_info["nonlin_calib_time"]*source_info["activity"],
                nbin = 290
                )
        hists.append(h_hit)
        full_hists.append(h_full_hit)
    total_hist = ROOT.TH1F('TotalSpectrum','Total Spectrum',290,0.1,3.0)
    total_hist.Sumw2()
    for hist in hists:
        total_hist.Add(hist,1)

    # define TF1
    mcshape = MulSimpleMCShape(2)
    pars = [
            3.446e5, 0.6130 , 1.522e-2  ,  2.685e3,
            2.881e5, 0.786  , 1.84e-2   ,  4.60e3,
            3.5e4  , 1.4253 , 3e-2      ,  4.5e2,
            2.159e4, 2.42   , 3.8e-2    ,  5.6e2
            ]

    pars_error = [0]*16

    # Fit Cs and Mn here
    A = ROOT.TF1("tmpa",mcshape,0.1,3.0,4*2)
    A.SetNpx(500)
    fit_lim_a = (0.4,0.9)
    for i,p in enumerate(pars):
        A.SetParameter(i,pars[i])
    s_a = total_hist.Fit(A,"S","",fit_lim_a[0], fit_lim_a[1])
    print(f"Chi2/Ndf = {s_a.Chi2():.2f}/{s_a.Ndf()}")
    for i in range(8):
        pars[i] = total_hist.GetFunction("tmpa").GetParameter(i)
        pars_error[i] = total_hist.GetFunction("tmpa").GetParError(i)
    # Fit K and Co here
    B = ROOT.TF1("tmpb",mcshape,0.1,3.0,4*2)
    B.SetNpx(500)
    for i,p in enumerate(pars):
        if i < 8:
            continue
        B.SetParameter(i-8,pars[i])
    fit_lim_b = (1.2, 2.7)
    s_b = total_hist.Fit(B,"S","", fit_lim_b[0], fit_lim_b[1])
    print(f"Chi2/Ndf = {s_b.Chi2():.2f}/{s_b.Ndf()}")
    for i in range(8):
        pars[i+8] = total_hist.GetFunction("tmpb").GetParameter(i)
        pars_error[i+8] = total_hist.GetFunction("tmpb").GetParError(i)

    # Calculate bias
    bias_info = {}
    for i,source in enumerate(sources):
        bias = 100*(pars[4*i+1] - full_hists[i].GetMean())/full_hists[i].GetMean()
        bias_error = 100*np.sqrt(pars_error[4*i+1]**2 + full_hists[i].GetMeanError()**2)/full_hists[i].GetMean()
        print(f"{source} : bias = {bias:.4f}, bias error = {bias_error:.4f}")
        bias_info[source] = {"bias":bias,"error":bias_error, "nPE":full_hists[i].GetMean()}

    # update config file!
    if update_config_file:
        for s,item in bias_info.items():
            config_data[s]["fit_bias"] = item["bias"]
            config_data[s]["uncertainty"] = item["error"]
            config_data[s]["nPE"] = item["nPE"]
        print("Update fit_bias, uncertainty, nPE in %s"%(config_file))
        save_yaml_data(config_data, config_file)


    # plot fig
    h_x,h_y = rhist2np(total_hist)
    x_a = h_x[(h_x >= fit_lim_a[0]) & (h_x < fit_lim_a[1])]
    total_y_a = [mcshape([x],pars[:8]) for x in x_a]
    x_b = h_x[(h_x >= fit_lim_b[0]) & (h_x < fit_lim_b[1])]
    total_y_b = [mcshape([x],pars[8:]) for x in x_b]
    fig = plt.figure()
    plt.errorbar(
            h_x,h_y,np.sqrt(h_y),
            linewidth=1,ms=2,fmt="o",
            label = "Simulated data",color = "black")
    plt.plot(x_a,total_y_a,
            label="Best fit",linewidth=3, color = "red")
    plt.plot(x_b,total_y_b,linewidth=3, color = "red")
    colors = ["#1f77b4","#ff7f0e","#2ca02c","#9467bd"]
    for index in range(len(sources)):
        npar = pars[index*4:index*4+4]
        if index < 2:
            # y_a = [mcshape.source_leak_spec([x],npar) for x in x_a]
            # plt.plot(x_a, y_a, "--", linewidth=2,color = colors[index + 2])
            y_a = [mcshape.source_spec([x],npar) for x in x_a]
            plt.plot(x_a, y_a,linestyle = "--",label=labels[index], linewidth=2, color = colors[index])
        else:
            # y_b = [mcshape.source_leak_spec([x],npar) for x in x_b]
            # plt.plot(x_b, y_b,"--", linewidth=2, color = colors[index + 2])
            y_b = [mcshape.source_spec([x],npar) for x in x_b]
            plt.plot(x_b, y_b,linestyle = "--",label=labels[index], linewidth=2, color = colors[index])
    plt.legend(fontsize=12,ncol=2)
    plt.yscale("log")
    plt.ylim(1.e2,1.e6)
    plt.xlabel("$E_{vis}$ [MeV]",fontsize=16)
    plt.ylabel("Counts per 10 keV",fontsize=16)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.tight_layout()
    fig_path = "../result/nonlinearity/fig/combine_source_spec_fit.eps"
    plt.savefig(fig_path)
    print("Fig save to %s"%(fig_path))
    plt.show()
    return bias_info

if __name__ == "__main__":
    fit_combinesource()
