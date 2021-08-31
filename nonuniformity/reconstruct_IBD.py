#!/usr/bin/python3
"""
    Reconstruct IBD
    ~~~~~~~~~~~~~~~~~~~~~~
    :author: Xu Hangkun (许杭锟)
    :copyright: © 2021 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""
import argparse
from utils import config,TaoNuMap,DataForReconstruct
from TaoDataAPI import TAOData
import os
import pickle

def reconstruct_IBD():

    parser = argparse.ArgumentParser()
    parser.add_argument('--IBD_dir', default="/dybfs/users/xuhangkun/SimTAO/offline/change_data/nonuniformity/positron_uni")
    parser.add_argument('--numap_path',default = config["idealmap_path"])
    parser.add_argument('--interp_mode',default = "linear")
    parser.add_argument('--output',default = "../result/nonuniformity/IBD_reconstructed_by_ideal_numap.pkl")
    args = parser.parse_args()
    print(args)

    # load nonuniformity map
    file = open(args.numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind=args.interp_mode)
    file.close()

    # Read Data
    files = os.listdir(args.IBD_dir)
    paths = [os.path.join(args.IBD_dir,f) for f in files]
    datas = TAOData(paths)
    data_recons = DataForReconstruct(datas,"positron")
    events = data_recons.get_normal_data(radius_cut = 650)

    # reconstruct
    reconstructed_events = tao_nu_map.reconstruct(events)

    # save the result
    file = open(args.output,"wb")
    pickle.dump(reconstructed_events,file)
    file.close()

if __name__ == "__main__":
    reconstruct_IBD()
