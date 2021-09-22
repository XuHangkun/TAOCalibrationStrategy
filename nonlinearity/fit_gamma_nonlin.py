# -*- coding: utf-8 -*-
"""
    fit gamma non-linearity
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""

import numpy as np
import argparse
from preprocess import GammaDataset
from nonlin_model import GammaChi2
from iminuit import Minuit
from utils import save_pickle_data

def fit_a_nonlin(chi2_func,init_pars = [0.9864364980986494,0.006350006360351107,0.04573173303523126]):
    """
    Find the smallest parameters
    """
    m = Minuit(chi2_func,
        p0=init_pars[0],
        p1=init_pars[1],
        p2=init_pars[2]
        )
    m.limits = [(0.5,1.5),(0.003,0.008),(0,1)]
    m.migrad()
    return m.values,m.errors

def fit_gamma_nonlin():
    parser = argparse.ArgumentParser(description='fit nonlinearity')
    parser.add_argument("--fit_mode", default="best",choices=["best","sigma_band"], help="fit model")
    parser.add_argument("--sys_err_times", default=100,type=int,help="time of do sys error change")
    parser.add_argument("--output", default="../result/nonlinearity/fit/fit_gamma_best_pars.pkl",help="output file to save the parameters")
    args = parser.parse_args()
    print(args)

    dataset = GammaDataset()
    fit_parameters = []
    if args.fit_mode == "best":
        info = dataset.get_data()
        g_chi2 = GammaChi2(info)
        g_chi2.errordef = Minuit.LEAST_SQUARES
        print("Start Fitting :")
        values,errors = fit_a_nonlin(g_chi2)
        chi2 = g_chi2(*list(values))
        print("\tBest Pars",values,"\n\tChi2",chi2)
        fit_parameters.append({"pars":list(values),"errors":list(errors),"chi2":chi2,"gamma_info":info})
    else:
        for i in range(args.sys_err_times):
            info = dataset.get_data(random_deviate = True)
            g_chi2 = GammaChi2(info)
            g_chi2.errordef = Minuit.LEAST_SQUARES
            print("Start Fitting :")
            values,errors = fit_a_nonlin(g_chi2)
            chi2 = g_chi2(*list(values))
            print("\tBest Pars",values,"\n\tChi2",chi2)
            fit_parameters.append({"pars":list(values),"errors":list(errors),"chi2":chi2,"gamma_info":info})

    save_pickle_data(fit_parameters,args.output)
    print("\tSave fit result to %s"%(args.output))

if __name__ == "__main__":
    fit_gamma_nonlin()
