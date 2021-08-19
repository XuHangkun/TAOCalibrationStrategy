import pandas as pd
from math import sin,cos,acos,asin
from utils import config

def create_idealmap_info():
    info = {
        "idx":[],
        "r":[],
        "theta":[],
        "phi":[],
        "calib_source":[],
        "file_name":[],
        "file_num":[],
        "energy":[]
    }
    for i in range(41):
        theta = acos(-1.0 + i*(2./40))
        theta = int(theta*180./3.1415926)
        for j in range(26):
            if j == 0:
                radius = 0
            else:
                delta_r3 = pow(900,3)/25.0
                radius = (pow(delta_r3*j,1./3) + pow(delta_r3*(j-1),1./3))/2.0
            info["idx"].append(len(info["idx"]))
            info["r"].append(radius)
            info["theta"].append(theta)
            info["phi"].append(0)
            info["calib_source"].append("electron")
            info["file_name"].append("e_theta%d_r%d.root"%(theta,radius))
            info["file_num"].append(1)
            info["energy"].append(1)
    info_df = pd.DataFrame(info)
    info_df.to_csv(config["idealmap_calib_info_path"],index=None)
    print("Calib info have been saved to %s"%(config["idealmap_calib_info_path"]))

if __name__ == "__main__":
    create_idealmap_info()
