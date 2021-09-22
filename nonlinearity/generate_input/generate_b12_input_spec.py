# -*- coding: utf-8 -*-
"""
    Generate b12 spectrum which will be used to do nonlinearity fitting
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Xu Hangkun (许杭锟)
    :copyright: © 2020 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""

import ROOT
import argparse
import os
import sys
sys.path.append("/dybfs/users/xuhangkun/SimTAO/offline")
from TaoDataAPI import TAOData
import pickle
from tqdm import tqdm
from utils import config

def GetEdepEvis(files):
    """
    Args:
        files : root files
        hist  : edep hist
    """
    edeps = []
    evises = []
    data = TAOData(files)
    data.SetBranchStatus(["*"],0)
    data.SetBranchStatus(["fNSiPMHit","fGdLSEdep"],1)
    for i in tqdm(range(data.GetEntries())):
        data.GetEntry(i)
        evis = data.GetAttr("fNSiPMHit")
        edep = data.GetAttr("fGdLSEdep")
        edeps.append(edep)
        evises.append(evis)
    return edeps,evises

parser = argparse.ArgumentParser(description="generate b12 spectrum")
parser.add_argument("--input_dir",default="/dybfs/users/xuhangkun/SimTAO/offline/change_data/neutron_design")
parser.add_argument("--input_file_num",default=100,type=int)
args = parser.parse_args()

evis_info = {"true_evis":[],"true_edep":[],"true_n12_evis":[],"true_n12_edep":[]}
# Evis info
input_files = []
for i in range(args.input_file_num):
    input_files.append(os.path.join(args.input_dir,"B12/B12_v%s.root"%(i)))
edeps,evises = GetEdepEvis(input_files)
for i in range(len(evises)):
    evis_info["true_evis"].append(evises[i]/config["energy_scale"])
    evis_info["true_edep"].append(edeps[i])

input_files = []
for i in range(args.input_file_num):
    input_files.append(os.path.join(args.input_dir,"N12/N12_v%s.root"%(i)))
edeps,evises = GetEdepEvis(input_files)
for i in range(len(evises)):
    evis_info["true_n12_evis"].append(evises[i]/config["energy_scale"])
    evis_info["true_n12_edep"].append(edeps[i])

afile = open("./input/b12_evis.pkl","wb")
pickle.dump(evis_info,afile)
afile.close()
