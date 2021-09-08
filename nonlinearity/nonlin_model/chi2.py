# -*- coding: utf-8 -*-
"""
    chi square of non-linearity fitting
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@163.com>
    :license: MIT, see LICENSE for more details.
"""

from .gamma_nonlin import GammaNL
from .continuous_spec_nonlin import ContinuousSpecNL
from utils import config
from math import pow
import copy

class GammaChi2:
    """chi square of gamma source
    """
    def __init__(self,info):
        """
        args:
            info : fit and bias information for gamma sources
                   eg:
                        info = {
                            "Ge68":{
                                "e_vis" : ~~~,
                                "e_true": ~~~,
                                "uncertainty":~~~
                            },
                            ...
                        }
        """
        self.info = info
        self.gamma_nonlin = GammaNL()

    def __call__(self,p0,p1,p2):
        """
        Args:
            p0 : A
            p1 : kb
            p2 : kc
        """
        chi2 = 0
        for key in self.info.keys():
            nonlin_factor = self.gamma_nonlin(key,p0,p1,p2)
            chi2 += pow((nonlin_factor*self.info[key]["e_true"] - self.info[key]["e_vis"])/self.info[key]["uncertainty"],2)
        return chi2

class ContinuousSpecChi2:
    """chi square of continuous spectrum
    """
    def __init__(self,
        evis_spec,
        edep_spec
        ):
        """
        Args:
            two hist : bin range [0,14], bin number 140
        """
        self.evis_spec = copy.deepcopy(evis_spec)
        self.cspec_nonlin = ContinuousSpecNL(edep_spec)

    def __call__(self,p0,p1,p2):
        """
        Args:
            p0 : A
            p1 : kb
            p2 : kc
        """
        chi2 = 0
        pred_hist = self.cspec_nonlin(p0,p1,p2)
        for bin_index in range(30,121):
            m = self.evis_spec.GetBinContent(bin_index)
            p = pred_hist.GetBinContent(bin_index)
            chi2 += pow(p-m,2)/m
        return chi2

class TotalChi2:
    """chi square of continuous spectrum and gamma
    """
    def __init__(self,
        gamma_info,
        evis_spec,
        edep_spec
        ):
        """
        Args:
            two hist : bin range [0,14], bin number 140
        """
        self.gamma_chi2 = GammaChi2(gamma_info)
        self.cspec_chi2 = ContinuousSpecChi2(evis_spec,edep_spec)

    def __call__(self,p0,p1,p2):
        """
        Args:
            p0 : A
            p1 : kb
            p2 : kc
        """
        return self.gamma_chi2(p0,p1,p2) + self.cspec_chi2(p0,p1,p2)
