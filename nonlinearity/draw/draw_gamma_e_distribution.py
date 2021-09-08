# -*- coding: utf-8 -*-
"""
    draw the figure of electron energy distribution
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""

import os
from utils.rhist2np import rhist2np
import ROOT
import numpy as np
import matplotlib.pyplot as plt

rfile = ROOT.TFile.Open("./input/gamma_electron_tao.root")
source_names = ["$^{68}Ge$","$^{137}Cs$","$^{54}Mn$","$^{40}K$","$^{60}Co$","$n-H$","$^{241}Am-^{12}C$"]
hist_names = ["hEGe","hECs","hEMn","hEK","hECo","hEnH","hEO16"]
for hist_name,source_name in zip(hist_names,source_names):
    hist = rfile.Get(hist_name)
    hist.Scale(10)
    x,y = rhist2np(hist)
    plt.plot(x,y,ds="steps-mid",label=source_name)
plt.legend()
plt.yscale("log")
plt.xlabel("Primary $e^{-}/e^{+}$ Kinetic [MeV]",fontsize=16)
plt.ylabel("Primary $e^{-}/e^{+}$ per $\gamma$ per keV",fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.ylim(1.e-4,1.)
plt.xlim(0,7)
plt.tight_layout()
save_path = "../result/nonlinearity/fig/gamma_electron_tao.eps"
plt.savefig(save_path)
print("Fig save to %s"%(save_path))
plt.show()
