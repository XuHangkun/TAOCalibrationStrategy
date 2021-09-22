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

class ContinuousSpecDataset:

    def __init__(self,
            evis_hits_file = "./input/b12_evis.pkl",
            spec_file = "./input/b12_spectrum.root",
            num_of_events = 100000
        ):
        # load data here
        self.evis_hits = read_pickle_data(evis_hits_file)
        self.spec_file = ROOT.TFile.Open(spec_file)
        self.edep_spec = self.spec_file.Get("b12_edep")
        self.edep_spec.SetDirectory(0)
        self.evis_spec = self.spec_file.Get("b12_evis")
        self.evis_spec.SetDirectory(0)
        self.spec_file.Close()
        self.num_of_events = num_of_events
        self.residual_bias = 0.3 # [%]
        self.initialize()
        print("Establish Continuous Spectrum dataset: \n\t%s\n\t%s"%(
                spec_file,evis_hits_file
            ))

    def initialize(self):
        self.edep_spec.Scale(1.0*self.num_of_events/self.edep_spec.Integral())
        self.evis_spec.Scale(1.0*self.num_of_events/self.evis_spec.Integral())
        for i in range(1,self.evis_spec.GetNbinsX()+1):
            content = self.evis_spec.GetBinContent(i)
            self.evis_spec.SetBinError(i,sqrt(1.0*content))

    def random_deviate(self,evis_spec):
        """ deviate nake E_vis according to each uncertainties.
        """
        evis_spec.Reset()
        sys_err = 2*(np.random.random()-0.5)
        rand_index = np.arange(0,len(self.evis_hits["true_evis"]))
        # np.random.shuffle(rand_index)
        for i in rand_index:
            evis = self.evis_hits["true_evis"][i]
            evis_spec.Fill((1 + self.residual_bias*sys_err/100)*evis)
        # consider the effect of statistic uncertainty
        for i in range(1,evis_spec.GetNbinsX()+1):
            content = evis_spec.GetBinContent(i)
            content = content + 2*(np.random.random() - 0.5)*sqrt(content)
            evis_spec.SetBinContent(i,1.0*content)
        # correct the bin uncertainty
        evis_spec.Scale(1.0*self.num_of_events/evis_spec.Integral())
        for i in range(1,evis_spec.GetNbinsX()+1):
            content = evis_spec.GetBinContent(i)
            evis_spec.SetBinError(i,sqrt(1.0*content))
        return evis_spec

    def get_data(self,random_deviate = False):
        edep_spec = copy.deepcopy(self.edep_spec)
        evis_spec = copy.deepcopy(self.evis_spec)
        if random_deviate:
            evis_spec = self.random_deviate(evis_spec)
        return evis_spec,edep_spec
