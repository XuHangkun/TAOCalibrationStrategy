from utils import config
from utils import MulMCShape,ELeakSpec,Gaus,read_gamma_hit
from TaoDataAPI import TAOData
import pandas as pd
import numpy as np
import ROOT
import time
import matplotlib.pyplot as plt
from utils import rhist2np

def fit_combinesource():
    # load data
    sources = ["Cs137","Mn54","K40","Co60"]
    energies = []
    labels = []
    hists = []
    for source in sources:
        source_info = config["radioactive_source"][source]
        energies.append(source_info["energy"])
        labels.append(source_info["label"])
        files = [source_info["file_path"]]
        h_hit = read_gamma_hit(
                source = source,
                files = files,
                energy = source_info["energy"],
                xrange = [0.1,3],
                num = source_info["calib_time"]*source_info["activity"]
                )
        hists.append(h_hit)
    total_hist = ROOT.TH1F('TotalSpectrum','Total Spectrum',300,0.1,3)
    total_hist.Sumw2()
    for hist in hists:
        total_hist.Add(hist,1)

    # define TF1
    spectrum_file = ROOT.TFile.Open("./input/All_Spec_wEnclosure.root")
    eleak_temps = [spectrum_file.Get("%s_leak"%(source)) for source in sources]
    mcshape = MulMCShape(
            sources = sources,
            energies = energies,
            eleak_temps = eleak_temps
            )
    A = ROOT.TF1("tmp",mcshape,0.1,3,4*len(sources))
    pars=[
        3.3e5,0.6,2.5,0.015,
        2.7e5,0.8,2.2,0.018,
        3.3e4,1.4,2.0,0.03,
        2.0e4,2.506,1.5,0.08
        ]
    for i in range(4*len(sources)):
        A.SetParameter(i,pars[i])
    A.SetNpx(500)

    # Fit
    total_hist.Fit(A,"S")

    # plot fig
    h_x,h_y = rhist2np(total_hist)
    pars = [total_hist.GetFunction("tmp").GetParameter(i) for i in range(4*len(sources))]
    total_y = [mcshape([x],pars) for x in h_x]
    source_specs = []
    for source in sources:
        source_y = [mcshape.source_spec(source,[x],pars) for x in h_x]
        source_specs.append(source_y)
    fig = plt.figure()
    plt.step(h_x,h_y,linewidth=2)
    plt.plot(h_x,total_y,label="Total")
    for index in range(len(sources)):
        plt.plot(h_x,source_specs[index],"--",label=labels[index])
    plt.legend(fontsize=12)
    plt.yscale("log")
    plt.ylim(1.e2,1.e6)
    plt.xlabel("$E_{vis}$ [MeV]",fontsize=16)
    plt.ylabel("Count",fontsize=16)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.tight_layout()
    fig_path = "../result/nonlinearity/fig/combine_source_spec_fit.eps"
    plt.savefig(fig_path)
    print("Fig save to %s"%(fig_path))
    plt.show()

if __name__ == "__main__":
    fit_combinesource()
