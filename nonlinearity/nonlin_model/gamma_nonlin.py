# -*- coding: utf-8 -*-
"""
    gamma nonlinearity
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@163.com>
    :license: MIT, see LICENSE for more details.
"""

from .electron_nonlin import ElectronNL
import numpy as np
from math import pow
from utils import config
import ROOT

class GammaNL:
    """Non-linearity of gamma
    """
    def __init__(self):
        """
        Gamma scintilation nonlinearity
        args:
            e_dis_file : root file contain electron distribution
        """
        self.e_dis_file = ROOT.TFile.Open(config["e_dis_file"])
        self.info = {}
        self.initialize()
        self.fnonlin = ElectronNL()

    def initialize(self):
        print("Initialize Gamma Non-linearity model :")
        ras_info = config["radioactive_source"]
        for key in ras_info.keys():
            self.info[key] = {}
            source_info = ras_info[key]
            self.info[key]["e_dis"] = self.e_dis_file.Get(source_info["e_dis_name"])
            end_bin = self.info[key]["e_dis"].FindBin(source_info["energy"])
            binw = self.info[key]["e_dis"].GetBinWidth(1)
            self.info[key]["e_dis_binw"]=binw
            x=np.zeros(self.info[key]["e_dis"].GetNbinsX())
            self.info[key]["e_dis"].GetXaxis().GetCenter(x)
            self.info[key]["e_dis_x"]=x[:end_bin]
            y = np.asarray(self.info[key]["e_dis"])[1:-1]
            self.info[key]["e_dis_y"]=y[:end_bin]
            print("\t",key,source_info["e_dis_name"],"End bin",end_bin,"Integral ",sum(y*x*binw))
            norm = 1.0/sum(y*x*binw)
            self.info[key]["norm"] = norm

    def __call__(self,key,p0,p1,p2):
        """calculate gamma non-linearity

        Returns:
            E_vis/E_dep
        """
        tmp = self.info[key]["e_dis_y"]*self.fnonlin(self.info[key]["e_dis_x"],p0,p1,p2)*self.info[key]["e_dis_x"]*self.info[key]["norm"]*self.info[key]["e_dis_binw"]
        evis_ratio = sum(tmp)
        return evis_ratio

if __name__ == "__main__":
    gamma_nl = GammaScintNL()
