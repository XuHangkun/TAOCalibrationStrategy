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
import ROOT

class ContinuousSpecWN12Dataset:

    def __init__(self,
            evis_hits_file = "./input/b12_evis.pkl",
            spec_file = "./input/b12_spectrum.root",
            num_of_events = 100000,
            n12_ratio = 0.028
        ):
        # read hit info for B12 and N12
        self.evis_hits = read_pickle_data(evis_hits_file)
        # read edep hist for B12 and N12
        self.spec_file = ROOT.TFile.Open(spec_file)
        self.edep_spec = self.spec_file.Get("b12_edep")
        self.edep_spec.SetDirectory(0)
        self.evis_spec = self.spec_file.Get("b12_evis")
        self.evis_spec.SetDirectory(0)
        self.n12_edep_spec = self.spec_file.Get("n12_edep")
        self.n12_edep_spec.SetDirectory(0)
        self.n12_evis_spec = self.spec_file.Get("n12_evis")
        self.n12_evis_spec.SetDirectory(0)
        self.spec_file.Close()
        self.num_of_events = num_of_events
        self.n12_ratio = n12_ratio
        self.residual_bias = 0.3 # [%]
        self.initialize()
        print("Establish Continuous Spectrum dataset: \n\t%s\n\t%s"%(
                spec_file,evis_hits_file
            ))

    def initialize(self):
        self.edep_spec.Scale(1.0*self.num_of_events/self.edep_spec.Integral())
        self.evis_spec.Scale(1.0*self.num_of_events/self.evis_spec.Integral())
        self.n12_edep_spec.Scale(1.0*self.num_of_events*self.n12_ratio/self.n12_edep_spec.Integral())
        self.n12_evis_spec.Scale(1.0*self.num_of_events*self.n12_ratio/self.n12_evis_spec.Integral())
        for i in range(1,self.evis_spec.GetNbinsX()+1):
            # b12 spectrum contaminated by n12 , and correct the error
            content = self.evis_spec.GetBinContent(i) + self.n12_evis_spec.GetBinContent(i)
            self.evis_spec.SetBinContent(i,content)
            self.evis_spec.SetBinError(i,sqrt(1.0*content))

    def random_deviate(self,evis_spec):
        """ deviate nake E_vis according to each uncertainties.
        """
        evis_spec.Reset()
        # sys_err = 2*(np.random.random()-0.5)
        sys_err = np.random.normal()
        rand_index = np.arange(0,len(self.evis_hits["true_evis"]))
        # fill b12 hit
        for i in rand_index:
            evis = self.evis_hits["true_evis"][i]
            evis_spec.Fill((1 + self.residual_bias*sys_err/100)*evis)
        # fill n12 hit
        for i in rand_index[:int(len(rand_index)*self.n12_ratio)]:
            evis = self.evis_hits["true_n12_evis"][i]
            evis_spec.Fill((1 + self.residual_bias*sys_err/100)*evis)
        # consider the effect of statistic uncertainty
        for i in range(1,evis_spec.GetNbinsX()+1):
            content = evis_spec.GetBinContent(i)
            content = content + 2*(np.random.random() - 0.5)*sqrt(content)
            evis_spec.SetBinContent(i,1.0*content)
        # correct the bin uncertainty
        evis_spec.Scale((1.0 + self.n12_ratio)*self.num_of_events/evis_spec.Integral())
        for i in range(1,evis_spec.GetNbinsX()+1):
            content = evis_spec.GetBinContent(i)
            evis_spec.SetBinError(i,sqrt(1.0*content))
        return evis_spec

    def get_data(self,random_deviate = False):
        edep_spec = copy.deepcopy(self.edep_spec)
        n12_edep_spec = copy.deepcopy(self.n12_edep_spec)
        evis_spec = copy.deepcopy(self.evis_spec)
        if random_deviate:
            evis_spec = self.random_deviate(evis_spec)
        return evis_spec,edep_spec,n12_edep_spec
