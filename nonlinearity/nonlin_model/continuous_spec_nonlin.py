# -*- coding: utf-8 -*-
"""
    continuous spectrum nonlinearity
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@163.com>
    :license: MIT, see LICENSE for more details.
"""
import numpy as np
from .electron_nonlin import ElectronNL
from math import pow,sqrt,exp
import ROOT
import copy
import pickle
from scipy import interpolate
from scipy import integrate
import pandas as pd

class ContinuousSpecNL:
    """Non-linearity of continuous spectrum
    """
    def __init__(self,
            edep_spec,
            e_res_file="./input/energy_resolution.csv",
            ):
        """
        args:
            edep_spec : ideal edep spec
        """
        self.edep_spec = edep_spec
        self.fnonlin = ElectronNL()
        # energy resolution model
        e_res_info = pd.read_csv(e_res_file)
        self.e_res_func = interpolate.interp1d(e_res_info["energy"],e_res_info["all"],kind="quadratic")
        self.sigma = 1.0
        self.mean = 3.0
        self.initialize()

    def initialize(self):
        print("Initialize Continuous Spectrum Non-linearity model ")
        # calculate some variable which can be use in furture
        self.es = [self.edep_spec.GetBinCenter(i) for i in range(1,self.edep_spec.GetNbinsX()+1)]
        self.ns = [self.edep_spec.GetBinContent(i) for i in range(1,self.edep_spec.GetNbinsX()+1)]
        self.pred_hist = ROOT.TH1F("pred_hist","pred_hist",140,0,14)
        self.pred_hist.SetDirectory(0)

    def energy_smear(self,x):
        # xx should be the evis
        return exp(-0.5*pow((x-self.mean)/self.sigma,2))/(sqrt(2*3.1415926)*self.sigma)

    def __call__(self,p0,p1,p2):
        """
        Args:
            p0 : A
            p1 : kb
            p2 : kc

        Return:
            xx,yy : Predicted spectrum
        """
        # Reset predict hist
        self.pred_hist.Reset()
        # calculate the non-linearity of electron
        pred_ratio = self.fnonlin(np.array(self.es),p0,p1,p2)
        for e,r,w in zip(self.es,pred_ratio,self.ns):
            # Add energy resolution here
            if e*r <2.7 or e*r > 12.5:
                continue
            the_bin = self.pred_hist.FindBin(e*r)
            self.mean = e*r
            self.sigma = self.e_res_func(e*r)*e*r
            n_range = int(self.sigma/self.pred_hist.GetBinWidth(1) + 1)
            for k in range(-3*n_range,3*n_range + 1):
                bin_low = self.pred_hist.GetBinCenter(the_bin+k) - 0.5*self.pred_hist.GetBinWidth(the_bin+k)
                bin_up = self.pred_hist.GetBinCenter(the_bin+k) + 0.5*self.pred_hist.GetBinWidth(the_bin+k)
                res_weight = integrate.quad(self.energy_smear,bin_low,bin_up)[0]
                self.pred_hist.AddBinContent(the_bin+k,w*res_weight)
        return self.pred_hist
