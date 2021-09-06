#!/usr/bin/python3
"""
    Reconstruct IBD
    ~~~~~~~~~~~~~~~~~~~~~~
    :author: Xu Hangkun (许杭锟)
    :copyright: © 2021 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""
import argparse
from utils import config,TaoNuMap,DataForReconstruct,gamma_fitable
from TaoDataAPI import TAOData
import os
import pickle

def reconstruct_IBD():

    parser = argparse.ArgumentParser()
    parser.add_argument('--IBD_dir', default="/dybfs/users/xuhangkun/SimTAO/offline/change_data/nonuniformity/positron_uni")
    parser.add_argument('--numap_path',default = config["idealmap_path"])
    parser.add_argument('--interp_mode',default = "cubic")
    parser.add_argument('--filter_points',action="store_true")
    parser.add_argument('--vertex_smear',default=0,type=float)
    parser.add_argument('--output',default = "../result/nonuniformity/IBD_reconstructed_by_ideal_numap.pkl")
    args = parser.parse_args()
    print(args)

    # load nonuniformity map
    file = open(args.numap_path,"rb")
    mapinfo = pickle.load(file)
    # we should add a filter here.
    if args.filter_points:
        filtered_mapinfo = []
        for item in mapinfo:
            if gamma_fitable(item["r"],item["theta"]):
                filtered_mapinfo.append(item)
        tao_nu_map = TaoNuMap(filtered_mapinfo,kind=args.interp_mode)
    else:
        tao_nu_map = TaoNuMap(mapinfo,kind=args.interp_mode)
    file.close()

    # Read Data
    files = os.listdir(args.IBD_dir)
    paths = [os.path.join(args.IBD_dir,f) for f in files]
    datas = TAOData(paths)
    data_recons = DataForReconstruct(datas,"positron")
    events = data_recons.get_normal_data(radius_cut = 650,
        vertex_resolution=args.vertex_smear)

    # reconstruct
    reconstructed_events = tao_nu_map.reconstruct(events)

    # save the result
    file = open(args.output,"wb")
    pickle.dump(reconstructed_events,file)
    file.close()

if __name__ == "__main__":
    reconstruct_IBD()