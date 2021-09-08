# -*- coding: utf-8 -*-
"""
    electron nonlinearity
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@163.com>
    :license: MIT, see LICENSE for more details.
"""

from math import exp
import numpy as np
import pandas as pd
import ROOT
from scipy import interpolate
from scipy import integrate
from math import pow
from utils import config

class ElectronNL:
    """Non-linearity model of electron
    """
    def __init__(self):
        self.cr_nl = CherenkovNL(
                config["cherenkov_file"]
                )
        self.scin_nl = ScintNL(
                config["de_dx_file"],
                config["scint_nonlin_map_file"]
                )

    def __call__(self,es,p0,p1,p2):
        """
        p0 : A
        p1 : kb
        p2 : kc
        """
        return p0*(self.scin_nl(es,p1)+self.cr_nl(es,p2))

class ScintNL:
    """non-linearity caused by liquid scintillator quenching.
    """
    def __init__(self,
            de_dx="./input/ESTAR_GdLS.txt",
            scint_nonlin_map_file="./input/scint_nonlin_map.csv",
            ):
        self.de_d_dx = pd.read_csv(de_dx)
        self.f_de_d_dx = interpolate.interp1d(self.de_d_dx["Kinetic"].to_numpy(),self.de_d_dx["Total"].to_numpy())
        self.kb = 0.0048
        self.kb2 = 1.5e-6
        self.interg_map = pd.read_csv(scint_nonlin_map_file)
        self.nonlin_func = interpolate.CloughTocher2DInterpolator(
                            list(zip(list(self.interg_map["es"]),list(self.interg_map["kb"]))),
                            list(self.interg_map["value"])
                            )

    def __call__(self,es,kb=0.0065,interg=False):
        """
        e should be a energy list in ascending order
        """
        if interg:
            return self.__call(es,kb)
        else:
            kbs = [kb for e in es]
            return np.array(self.nonlin_func(es,kbs))

    def __call(self,es,kb=0.0065,kb2=1.5e-6):
        """
        e should be a energy list in ascending order
        """
        self.kb = kb
        self.kb2 = kb2
        nes = np.concatenate((np.array([0]),es),axis=0)
        accum = 0.
        value = []
        for i in range(len(es)):
            accum += integrate.quad(self.dscintnl,nes[i],nes[i+1])[0]
            value.append(accum/nes[i+1])
        return np.array(value)

    def dscintnl(self,es):
        return 1./(1 + self.kb*self.f_de_d_dx(es) + pow(self.kb2*self.f_de_d_dx(es),2))

    def generate_map(self,kb_lim=[0.0010,0.010],step=0.00002):
        """
        generate f_scint(E,kb) map
        """
        info = {
                "es":[],
                "kb":[],
                "value":[]
                }
        es = [0.001*i for i in range(100)] + [0.1 + j*0.01 for j in range(90)] + [1+0.1*k for k in range(140)]
        es[0] = 1.e-5
        for i in range(1000):
            kb = kb_lim[0] + step*i
            if kb > kb_lim[1]:
                break
            kbs = [kb for e in es]
            value = self.__call(es,kb)
            info["es"] += es
            info["kb"] += kbs
            info["value"] += list(value)
        return info

class CherenkovNL:
    """ non-linearity caused by Cherenkov process
    """
    def __init__(self,cherenkov_file="./input/TAO_Cherenkov.csv"):
        self.cherenkov = pd.read_csv(cherenkov_file)
        self.f_cherenkov = interpolate.interp1d(
                            self.cherenkov["energy"].to_numpy(),
                            self.cherenkov["cov"].to_numpy()
                            )

    def __call__(self,e,kc):
        return self.f_cherenkov(e)*kc
