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
from preprocess import GammaDataset,ContinuousSpecDataset
from nonlin_model import TotalChi2
from iminuit import Minuit
from utils import save_pickle_data

def fit_a_nonlin(chi2_func,init_pars = [0.99,5.3e-3,4.21e-2]):
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

def fit_total_nonlin():
    parser = argparse.ArgumentParser(description='fit nonlinearity')
    parser.add_argument("--fit_mode", default="best",choices=["best","sigma_band"], help="fit model")
    parser.add_argument("--sys_err_times", default=30,type=int,help="time of do sys error change")
    parser.add_argument("--output", default="../result/nonlinearity/fit/fit_total_best_pars.pkl",
            help="output file to save the parameters")
    args = parser.parse_args()
    print(args)

    gamma_dataset = GammaDataset()
    cspec_dataset = ContinuousSpecDataset()
    fit_parameters = []
    if args.fit_mode == "best":
        gamma_info = gamma_dataset.get_data()
        cspec_evis,cspec_edep = cspec_dataset.get_data()
        g_chi2 = TotalChi2(gamma_info,cspec_evis,cspec_edep)
        g_chi2.errordef = Minuit.LEAST_SQUARES
        print("Start Fitting :")
        values,errors = fit_a_nonlin(g_chi2)
        chi2 = g_chi2(*list(values))
        print("\tBest Pars",values,"\n\tChi2",chi2)
        fit_parameters.append({"pars":list(values),"errors":list(errors),"chi2":chi2,"gamma_info":gamma_info})
    else:
        for i in range(args.sys_err_times):
            gamma_info = gamma_dataset.get_data(random_deviate = True)
            cspec_evis,cspec_edep = cspec_dataset.get_data(random_deviate = True)
            g_chi2 = TotalChi2(gamma_info,cspec_evis,cspec_edep)
            g_chi2.errordef = Minuit.LEAST_SQUARES
            print("Start Fitting :")
            values,errors = fit_a_nonlin(g_chi2)
            chi2 = g_chi2(*list(values))
            print("\tBest Pars",values,"\n\tChi2",chi2)
            fit_parameters.append({"pars":list(values),"errors":list(errors),"chi2":chi2,"gamma_info":gamma_info})

    save_pickle_data(fit_parameters,args.output)
    print("\tSave fit result to %s"%(args.output))

if __name__ == "__main__":
    fit_total_nonlin()
