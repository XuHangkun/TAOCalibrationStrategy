from utils import config
from utils import MCShape,ELeakSpec,Gaus,read_gamma_hit
from TaoDataAPI import TAOData
import pandas as pd
import numpy as np
import ROOT
import time
import matplotlib.pyplot as plt
from utils import rhist2np

def fit_ge68():
    # load data
    ge68_info = config["radioactive_source"]["Ge68"]
    files = [ge68_info["file_path"]]
    h_hit = read_gamma_hit(
            source = "Ge68",
            files = files,
            energy = ge68_info["energy"],
            num = ge68_info["calib_time"]*ge68_info["activity"]
            )
    # define TF1
    spectrum_file = ROOT.TFile.Open("./input/All_Spec_wEnclosure.root")
    eleak_temp = spectrum_file.Get("Ge68_leak")
    mcshape = MCShape(
            source = "Ge68",
            energy = ge68_info["energy"],
            eleak_temp = eleak_temp
            )
    A = ROOT.TF1("tmp",mcshape,0,1.1*ge68_info["energy"],4)
    A.SetParameters(2200,0.95,2.0,0.04)
    A.SetNpx(500)

    # Fit
    h_hit.Fit("tmp","SR")

    # plot fig
    h_x,h_y = rhist2np(h_hit)
    pars = [h_hit.GetFunction("tmp").GetParameter(i) for i in range(4)]
    eleak_y = [mcshape.leak_energy_spec([x],pars) for x in h_x]
    total_y = [mcshape([x],pars) for x in h_x]
    fig = plt.figure()
    plt.step(h_x,h_y,linewidth=2)
    plt.plot(h_x,total_y,label="Total")
    plt.plot(h_x,eleak_y,"--",label="Energy leak")
    plt.legend()
    plt.xlabel("$E_{vis}$ [MeV]",fontsize=16)
    plt.ylabel("Count",fontsize=16)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.tight_layout()
    fig_path = "../result/nonlinearity/fig/ge68_spec_fit.eps"
    plt.savefig(fig_path)
    print("Fig save to %s"%(fig_path))
    plt.show()

if __name__ == "__main__":
    fit_ge68()
