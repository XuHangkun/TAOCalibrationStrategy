from math import sqrt,pow,asin,acos,atan,sin,cos,tan
import numpy as np
import pandas as pd
import copy
from .tools import rthetaphi2xyz,xyz2rthetaphi

def generate_pointcalib_info(
        ideal_map,
        anchor_1,
        anchor_2,
        num_per_line=100,
        max_radius=850,
        min_distance=25,
        max_distance=50,
        min_value_diff=0.01,
        symmetry = False
        ):
    """save init points which will be used to do optimize and calibration
    Args:
        map : tao nonuniformity map
        anchor_1 : position info of the first anchor : {"theta":30,"phi":73}
        anchor_2 : position info of second anchor
    Returns:
        point information
    """
    info = {
        "r": [],
        "theta": [],
        "phi": [],
        "realistic":[],
        "calib_source":[],
        "file_name":[],
        "file_num":[],
        "energy":[]
    }
    # center point for ge68
    info["r"] += [0 for x in range(0,51)]
    info["theta"] += [x*180/50 for x in range(0,51)]
    info["phi"] += [0 for x in range(0,51)]
    info["realistic"] += [False for x in range(0,51)]
    info["realistic"][0] = True
    info["calib_source"] += ["ge68" for x in range(0,51)]

    # center point for cs137
    info["r"] += [0]
    info["theta"] += [0]
    info["phi"] += [0]
    info["realistic"] += [True]
    info["calib_source"] += ["cs137"]

    # center line for ge68
    info["r"] +=  [100,200,300,400,500,550,600,650,700,750,800,850]
    info["theta"]  +=  [180,180,180,180,180,180,180,180,180,180,180,180]
    info["phi"]    +=  [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
    info["realistic"]    +=  [  True,  True,  True,  True,  True,  True,  True,
            True,  True,  True,  True,  True]
    info["calib_source"] += ["ge68" for i in range(12)]
    
    info["r"] += [100,200,300,400,500,550,600,650,700,750,800,850]
    info["theta"] +=  [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0]
    info["phi"] +=  [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0]
    info["realistic"]    +=  [  True,  True,  True,  True,  True,  True,  True,
            True,  True,  True,  True,  True]
    info["calib_source"] += ["ge68" for i in range(12)]

    # CLS line for Cs137
    nodes = [
            rthetaphi2xyz(900,2.865,0),
            rthetaphi2xyz(anchor_1["r"],anchor_1["theta"],anchor_1["phi"]),
            rthetaphi2xyz(anchor_2["r"],anchor_2["theta"],anchor_2["phi"]),
            rthetaphi2xyz(900,2.865,180)
            ]
    b_point = [0,0,900]
    b_value = 0.
    for i in range(len(nodes)-1):
        index_1 = i % len(nodes)
        index_2 = (i + 1) % len(nodes)
        for j in range(1,num_per_line+1):
            point = nodes[index_1] + j * (nodes[index_2] - nodes[index_1]) / num_per_line
            distance = sqrt(sum([pow(x-y,2) for x,y in zip(b_point,point)]))
            r_t_p = xyz2rthetaphi(point[0],point[1],point[2])
            radius = r_t_p[0]
            theta = r_t_p[1]
            phi=r_t_p[2]
            dis_value = abs(ideal_map(radius,theta) - b_value)
            if distance < min_distance or radius > max_radius:
                continue

            if distance < max_distance and dis_value < min_value_diff:
                continue

            b_point = copy.deepcopy(point)
            b_value = ideal_map(radius,theta)

            length = sqrt(sum([pow(x-y,2) for x,y in zip(nodes[index_2],nodes[index_1])]))
            direction = (nodes[index_2] - nodes[index_1])/length

            info["r"].append(radius)
            info["theta"].append(theta)
            info["phi"].append(phi)
            info["realistic"].append(True)
            info["calib_source"].append("cs137")
            if symmetry:
                info["r"].append(radius)
                info["theta"].append(180 - theta)
                info["phi"].append(phi)
                info["realistic"].append(False)
                info["calib_source"].append("cs137")
    
    # add file name and file_num here
    for i in range(len(info["calib_source"])):
        info["file_name"].append("%s_r%d_theta%d_phi%d"%(
            info["calib_source"][i],info["r"][i],info["theta"][i],info["phi"][i]
        ) + "_v%d.root")
        info["file_num"].append(10)
        if info["calib_source"][i] == "ge68":
            info["energy"].append(2*0.511)
        else:
            info["energy"].append(0.617)

    # datas = []
    # for i in range(len(info["r"])):
        # item = {}
        # item["r"] = info["r"][i]
        # item["theta"] = info["theta"][i]
        # item["phi"] = info["phi"][i]
        # item["realistic"] = info["realistic"][i]
        # item["calib_source"] = info["calib_source"][i]
        # item["nu_value"] = ideal_map(item["r"],item["theta"])
        # datas.append(item)
    info_df = pd.DataFrame(info)
    print(info_df)
    return info_df