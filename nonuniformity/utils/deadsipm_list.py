from .config import config
import numpy as np
import pandas as pd

def is_contained(theta,phi,sipm_dead_mode ="all"):
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
    if sipm_dead_mode  == "all":
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

def generate_dead_sipm(sipm_dead_mode ="all"):
    """generate the list of dead sipm id

    Args:
        sipm_dead_mode  : keep the dead sipm in one hemisphere
    """
    np.random.seed(7)
    sipm_pos_info = pd.read_csv(config["sipm_pos_file"])
    total_sipm = len(sipm_pos_info)
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
    return dead_list

def test():
    dead_list = generate_dead_sipm()
    print(len(dead_list))

if __name__ == "__main__":
    test()
