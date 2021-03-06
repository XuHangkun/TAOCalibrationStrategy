#!/usr/bin/python3
"""
    Create nonuniformity map
    ~~~~~~~~~~~~~~~~~~~~~~
    :author: Xu Hangkun (许杭锟)
    :copyright: © 2021 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""

from .config import config
from .deadsipm_list import generate_dead_sipm
import copy
import pandas as pd
import ROOT
from TaoDataAPI import TAOData
import os
import numpy as np
from tqdm import tqdm
from collections import Counter

def cal_full_hit(data,
    energy,
    sipm_dead_mode = None,
    sipm_dead_seed = 7
    ):

    data.SetBranchStatus(["*"],0)
    if not sipm_dead_mode:
        data.SetBranchStatus(["fGdLSEdep","fNSiPMHit"],1)
        dead_list = []
        adjs = []
    else:
        data.SetBranchStatus(["fGdLSEdep","fNSiPMHit","fSiPMHitID"],1)
        dead_list,adjs = generate_dead_sipm(sipm_dead_mode,sipm_dead_seed)

    hit_list = []
    for i in range(data.GetEntries()):
        data.GetEntry(i)
        edep = data.GetAttr("fGdLSEdep")
        hit = data.GetAttr("fNSiPMHit")
        if edep < energy*0.9998:
            continue
        else:
            if sipm_dead_mode:
                hit_ids = data.GetAttr("fSiPMHitID")
                # minus dead sipm
                hit_ids_counter = Counter(hit_ids)
                for d_sipm,d_adj in zip(dead_list,adjs):
                    nhit -= hit_ids_counter[d_sipm]

                    # correct by adjacent readout channels
                    adj_hits = []
                    for j in d_adj:
                        adj_hits.append(hit_ids_counter[j])
                    adj_hit = np.mean(adj_hits)
                    nhit += adj_hit
            hit_list.append(hit)
    return hit_list

def generate_numap(
    calibration_data,
    file_dir,
    symmetry = False,
    sipm_dead_mode = None,
    sipm_dead_seed = 7
    ):
    """generate nonuniformity map

    Args:
        calibration_data : data contain calibration info
            idx   :  unique index
            r : ...
            theta : ...
            phi : calibration position infomation
            calib_source : electron , cs137 or ge68
            file_name : for eg. electron_v%d.root
            file_num  : number of file
        file_dir : dir which store the root file
        symmetry : if we think the detector is up-down symmetry
        sipm_dead_mode : control the dead sipm position
            all , left , right , up and down
    """
    # load csv data and convert data
    calibration_data = copy.deepcopy(calibration_data)
    data_len = len(calibration_data)
    calibration_data = calibration_data.to_dict()
    data_lists = []

    # calculate the calibration info
    reference_info = {
        "calib_source":[],
        "mean_full_hit":[]
    }
    for i in tqdm(range(data_len)):
        item = {}
        for key in calibration_data.keys():
            item[key] = calibration_data[key][i]

        if not item["realistic"] and item["r"] < 1:
            item["mean_full_hit"] = reference_info["mean_full_hit"][reference_info["calib_source"].index(item["calib_source"])]
            item["std_full_hit"] = 0
            item["nu_value"] = 1.0
            data_lists.append(item)
            continue

        if item["file_num"] > 1:
            files = [
                os.path.join(file_dir,item["file_name"]%(j)) for j in range(item["file_num"])
                ]
        else:
            files = [os.path.join(file_dir,item["file_name"])]
        exists_files = [e_file for e_file in files if os.path.exists(e_file)]
        print("r %d theta %d file num %d"%(item["r"],item["theta"],len(exists_files)))
        data = TAOData(exists_files)
        full_hit_list = cal_full_hit(
                data,energy = item["energy"],
                sipm_dead_mode=sipm_dead_mode,
                sipm_dead_seed=sipm_dead_seed
                )
        # save the info
        item["full_hit_list"] = full_hit_list
        item["realistic"] = True
        item["mean_full_hit"] = np.mean(full_hit_list)
        item["std_full_hit"] = np.std(full_hit_list)
        if item["r"] < 900:
            if item["calib_source"] not in reference_info["calib_source"]:
                reference_info["calib_source"].append(item["calib_source"])
                reference_info["mean_full_hit"].append(item["mean_full_hit"])

        item["nu_value"] = 1.0
        data_lists.append(item)

    # calculate the value
    for item in data_lists:
        index = reference_info["calib_source"].index(item["calib_source"])
        item["nu_value"] = item["mean_full_hit"]/reference_info["mean_full_hit"][index]

    # consider the symmetry
    if symmetry:
        sym_datas = []
        start_id = len(data_lists) + 1
        for oitem in data_lists:
            if oitem["theta"] < 0.1 or oitem["theta"] > 179.9 or oitem["r"] < 0.1:
                continue
            item = copy.deepcopy(oitem)
            item["realistic"] = False
            item["theta"] = 180 - item["theta"]
            item["idx"] = start_id
            start_id += 1
            sym_datas.append(item)
        data_lists += sym_datas

    return data_lists
