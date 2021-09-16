from .config import config
import numpy as np
import pandas as pd
from .tools import rthetaphi2xyz
from math import sin,sqrt

def is_contained(theta,phi,sipm_dead_mode ="uni"):
    """
    Args:
        sipm_dead_mode  : position of sipm
                up : 0 < theta < 90
                down : 90 < theta < 180
                left : 180 < phi < 360
                right : 0 < phi < 180
    Return :
        True or False
    """
    if sipm_dead_mode  == "uni":
        return True

    if sipm_dead_mode  == "up":
        if 0 < theta and theta < 90:
            return True
    elif sipm_dead_mode  == "down":
        if 90 < theta and theta < 180:
            return True
    elif sipm_dead_mode  == "left":
        if 180 < phi and phi < 360:
            return True
    elif sipm_dead_mode  == "right":
        if 0 < phi and phi < 180:
            return True
    else:
        return False

def generate_dead_sipm(sipm_dead_mode ="uni",seed=7):
    """generate the list of dead sipm id

    Args:
        sipm_dead_mode  : keep the dead sipm in one hemisphere
    """
    print("Generate dead sipm list , dead mode : %s , dead seed : %d."%(sipm_dead_mode,seed))
    np.random.seed(seed)
    sipm_pos_info = pd.read_csv(config["sipm_pos_file"])
    total_sipm = len(sipm_pos_info)

    # generate dead readout channels randomly
    dead_list = []
    while True:
        sipm_id = int(np.random.random()*total_sipm)
        if sipm_id in dead_list:
            continue
        sipm_theta = sipm_pos_info["theta"][sipm_id]
        sipm_phi = sipm_pos_info["phi"][sipm_id]
        if is_contained(sipm_theta,sipm_phi,sipm_dead_mode ):
            dead_list.append(sipm_id)
        if len(dead_list) >= round(total_sipm*config["dead_sipm_ratio"]):
            break

    # get adjacent sipms
    adjs = []
    for item in dead_list:
        adj_index = generate_adj_sipm(item,sipm_pos_info)
        f_indexs = []
        for j in adj_index:
            if j not in dead_list:
                f_indexs.append(j)
        adjs.append(f_indexs)

    return dead_list,adjs

def generate_adj_sipm(sipm_index,pos_data):
    pos = [930,pos_data["theta"][sipm_index],pos_data["phi"][sipm_index]]
    sipm_num = len(pos_data)
    adjs_index = []
    for i in range(sipm_index - 500, sipm_index + 500):
        if i < 0 or i >= sipm_num or i == sipm_index :
            continue
        theta = pos_data["theta"][i]
        phi = pos_data["phi"][i]
        if abs(theta - pos[1]) > 4:
            continue
        r_phi_len = abs(pos[0]*sin(pos[1]*3.1415926/180)*(pos[2] - phi)*3.1415926/180)
        r_theta_len = abs(pos[0]*(pos[1] - theta)*3.1415926/180)
        if sqrt(r_phi_len*r_phi_len + r_theta_len*r_theta_len) > 65:
            continue
        adjs_index.append(i)
    return adjs_index

def test():
    dead_list = generate_dead_sipm()
    print(len(dead_list))

if __name__ == "__main__":
    test()
