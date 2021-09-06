#!/usr/bin/python3
"""
    Optimize anchor position
    ~~~~~~~~~~~~~~~~~~~~~~
    :author: Xu Hangkun (许杭锟)
    :copyright: © 2021 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""

import pandas as pd
from utils import TaoNuMap,AnchorOptimizer
import ROOT
import argparse
import os
import copy
import sys
import numpy as np
from tqdm import tqdm
from math import sin,cos
from utils import config
import pickle
import json

parser = argparse.ArgumentParser(description="energy reconstruction")
parser.add_argument("--ideal_nu_map",default=config["idealmap_path"])
parser.add_argument("--max_radius",default=700,type=float)
parser.add_argument("--rough_search_times",default=3000,type=int)
parser.add_argument("--care_search_times",default=1000,type=int)
parser.add_argument("--no_symmetry",action="store_true")
parser.add_argument("--optimize_chi2_info",default="../result/nonuniformity/optimize_anchor_position.csv")
parser.add_argument("--best_anchor_position_file",default="../result/nonuniformity/best_anchors.json")
args = parser.parse_args()
print(args)
np.random.seed(7)

file = open(args.ideal_nu_map,"rb")
mapinfo = pickle.load(file)
ideal_nu_map = TaoNuMap(mapinfo,kind="cubic")

optimizer = AnchorOptimizer(
    ideal_map=ideal_nu_map,
    symmetry=not args.no_symmetry,
    max_radius=args.max_radius
)
# optimize the anchor roughly
optimize_info = optimizer.scan_anchor_params(num=args.rough_search_times)
min_index = np.argmin(optimize_info["chi2"].to_numpy())
value = optimize_info.loc[min_index,["theta_1","theta_2","phi_2"]].to_numpy()
print("Roughly best : ",value)

# optimzie the anchor carefully
care_optimize_info = optimizer.scan_anchor_params(
    par_lim = [(value[0]-5,value[0]+5),(value[1]-5,value[1]+5),(value[2]-5,value[2]+5)],
    num=args.care_search_times
    )
min_index = np.argmin(care_optimize_info["chi2"].to_numpy())
care_value = care_optimize_info.loc[min_index,["theta_1","theta_2","phi_2"]].to_numpy()
print("Carefully best : ",value)

# store information
optimize_info = pd.concat([optimize_info,care_optimize_info],axis=0)
optimize_info.to_csv(args.optimize_chi2_info,index=None)
best_anchor_info = {"rough_optim_param":value,"care_optim_param":care_value}
f = open(args.best_anchor_position_file,"w")
json.dump(best_anchor_info,f)
f.close()