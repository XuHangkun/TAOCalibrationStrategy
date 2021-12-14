# -*- coding: utf-8 -*-
"""
    Gamma Dataset
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""
import pickle
import numpy as np
from math import pow,sqrt
from utils import config,read_pickle_data
import copy

class GammaDataset:

    def __init__(self,
        ra_fit_info = "./input/ra_fit_info.pkl",
        shadowing_info = "./input/shadowing_info.pkl",
        nake_true_info = "./input/nake_true_info.pkl"
        ):
        self.ra_fit_info = read_pickle_data(ra_fit_info)
        self.shadowing_info = read_pickle_data(shadowing_info)
        self.nake_true_info = read_pickle_data(nake_true_info)
        self.O16_bias = 0.4 # [%]
        self.residual_bias = 0.3 # [%]
        self.scale = self.nake_true_info["nH"]["nake_evis"]/config["radioactive_source"]["nH"]["energy"]
        self.info = {}
        self.initialize()
        print("Establish gamma dataset: \n\t%s\n\t%s\n\t%s"%(
                nake_true_info,ra_fit_info,shadowing_info
            ))

    def initialize(self):
        ra_config = config["radioactive_source"]
        for key in ra_config:
            error = sqrt(
                pow(self.ra_fit_info[key]["fit_bias"]*self.nake_true_info[key]["nake_evis"]/100,2) +
                pow(self.shadowing_info[key]["shadowing"]*self.nake_true_info[key]["nake_evis"]/100,2) +
                pow(self.residual_bias*self.nake_true_info[key]["nake_evis"]/100,2) +
                pow(self.nake_true_info[key]["nake_evis_e"],2)
                )
            if key == "O16":
                error = sqrt(error*error + pow(self.O16_bias*self.nake_true_info[key]["nake_evis"]/100,2))
            self.info[key] = {
                "e_true":self.nake_true_info[key]["total_gamma_e"],
                "e_vis":self.nake_true_info[key]["nake_evis"]/self.scale,
                "uncertainty":error/self.scale
            }

    def random_deviate(self,info):
        """ deviate nake E_vis according to each uncertainties.
        """
        sys_err_control={"shadowing":0,"fit":0,"pd_eff":0,"p_recoil":0}
        for key in sys_err_control.keys():
            # sys_err_control[key] = 2*(np.random.random()-0.5)
            sys_err_control[key] = np.random.normal()
        for key in info.keys():
            # fit bias
            info[key]["e_vis"] += sys_err_control["fit"]*self.ra_fit_info[key]["fit_bias"]*self.nake_true_info[key]["nake_evis"]/(self.scale*100)
            # fit bias
            info[key]["e_vis"] += sys_err_control["shadowing"]*self.shadowing_info[key]["shadowing"]*self.nake_true_info[key]["nake_evis"]/(self.scale*100)
            info[key]["e_vis"] += sys_err_control["pd_eff"]*self.residual_bias*self.nake_true_info[key]["nake_evis"]/(self.scale*100)
            if key == "O16":
                info[key]["e_vis"] += sys_err_control["p_recoil"]*self.O16_bias*self.nake_true_info[key]["nake_evis"]/(self.scale*100)
        return info

    def get_data(self,random_deviate = False):
        info = copy.deepcopy(self.info)
        if random_deviate:
            self.random_deviate(info)
        return info
