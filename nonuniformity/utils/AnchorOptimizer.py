"""
    Chi2 of anchor optimizer
    ~~~~~~~~~~~~~~~~~~~~~~
    :author: Xu Hangkun (许杭锟)
    :copyright: © 2021 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""
from .TaoNuMap import TaoNuMap
import numpy as np
from math import sqrt,sin,cos,acos
from tqdm import trange
import pandas as pd
import copy

def xyz2rthetaphi(x,y,z):
    """convert x,y,z to radiu,theta,phi
    """
    radius = sqrt(x*x + y*y + z*z)
    theta = acos(z/radius)*180./3.1415926
    if x < 1.e-5 and y < 1.e-5:
        phi = 0
    else:
        phi = acos(x/sqrt(x*x + y*y))*180./3.1415926
    if y < 0:
        phi = 360 - phi
    return np.array([radius,theta,phi])

def rthetaphi2xyz(radius,theta,phi):
    """convert radius,theta,phi to x,y,z
    """
    theta *= 3.1415926/180
    phi *= 3.1415926/180
    z = radius * cos(theta)
    x = radius * sin(theta) * cos(phi)
    y = radius * sin(theta) * sin(phi)

    return np.array([x,y,z])

def create_numap_byidealline(
    ideal_map,
    first_anchor,
    second_anchor,
    symmetry = True,
    num_per_line=200
    ):
    """
    Args:
        ideal_map : ideal map
        first anchor : eg. {"r":900,"theta":152,"phi":0}
        second anchor: same as the first anchor
        symmetry : if we assume up-down symmetry
        num_per_line : ideal calibration point number per line
    """
    # calculate the points along the line here
    radius_cut = 850
    info = {
        "radius":[],
        "theta":[],
        "realistic":[]
    }
    # ACU points
    # center point
    info["radius"] += [0 for x in range(1,num_per_line)]
    info["theta"] += [x*180/num_per_line for x in range(1,num_per_line)]

    # center line
    info["radius"] += [x*900./num_per_line for x in range(num_per_line+1)]
    info["theta"] += [0 for x in range(num_per_line+1)]

    info["radius"] += [x*900./num_per_line for x in range(num_per_line+1)]
    info["theta"] += [180 for x in range(num_per_line+1)]

    nodes = [
            rthetaphi2xyz(900,0,0),
            rthetaphi2xyz(second_anchor["r"],first_anchor["theta"],first_anchor["phi"]),
            rthetaphi2xyz(second_anchor["r"],second_anchor["theta"],second_anchor["phi"])
            ]

    for i in range(len(nodes)):
        index_1 = i % len(nodes)
        index_2 = (i + 1) % len(nodes)
        for j in range(1,num_per_line):
            point = nodes[index_1] + j * (nodes[index_2] - nodes[index_1]) / num_per_line
            r_t_p = xyz2rthetaphi(point[0],point[1],point[2])
            radius = r_t_p[0]
            theta = r_t_p[1]
            info["radius"].append(radius)
            info["theta"].append(theta)

    ideal_calib_infos = []
    for i in range(len(info["radius"])):
        if info["radius"][i] > 850:
            continue
        item = {}
        item["r"] = info["radius"][i]
        item["theta"] = info["theta"][i]
        item["nu_value"] = ideal_map(item["r"],item["theta"])
        item["realistic"] = True
        ideal_calib_infos.append(item)
        if symmetry:
            if item["theta"] <= 0.1 or item["theta"] >= 179.9:
                pass
            else:
                s_item = copy.deepcopy(item)
                s_item["theta"] = 180 - s_item["theta"]
                s_item["realistic"] = False
                ideal_calib_infos.append(s_item)

    # make new nu map
    new_nu_map = TaoNuMap(ideal_calib_infos)
    return new_nu_map

class AnchorOptimizer:
    """Chi2 which can be used to optimize anchor position
    """

    def __init__(self,ideal_map,
        symmetry=True,
        anchor_radius = 900,
        max_radius=700,
        n_theta = 100,
        n_radius = 100
        ):
        self.ideal_map = ideal_map
        self.symmetry = symmetry
        self.max_radius = max_radius
        self.ntheta = n_theta
        self.nradius = n_radius
        self.anchor_radius = anchor_radius

    def __call__(self,first_anchor,second_anchor):
        new_map = create_numap_byidealline(
            self.ideal_map,
            first_anchor=first_anchor,
            second_anchor=second_anchor,
            symmetry=self.symmetry
        )
        chi2 = self.mapdiffchi2(self.ideal_map,new_map)
        return chi2

    def mapdiffchi2(self,first_map,second_map):
        """calculate difference between two map
        """
        delta_r3 = pow(self.max_radius,3)/self.nradius
        delta_cos = 2./self.ntheta
        radiuss = []
        thetas = []
        for i in range(self.nradius):
            radiu = (pow(i*delta_r3,1./3)+pow((i + 1) * delta_r3,1./3))/2
            for j in range(1,self.ntheta):
                theta = 180*acos(1 - j*delta_cos)/3.1415926
                if theta < 0.1:
                    theta = 0.1
                if theta > 179.9:
                    theta = 179.9
                radiuss.append(radiu)
                thetas.append(theta)
        radiuss = np.array(radiuss)
        thetas = np.array(thetas)
        nu_value_1 = first_map(radiuss,thetas)
        nu_value_2 = second_map(radiuss,thetas)
        chi2 = np.power(nu_value_1-nu_value_2,2)
        chi2 = np.mean(chi2)
        return 1.e6*chi2

    def scan_anchor_params(self,
        par_name=["theta_1","theta_2","phi_2"],
        par_lim=[(90,125),(130,170),(151,152)],
        num = 10000):
        info = {"chi2":[]}
        for name in par_name:
            info[name] = []
        # scan the parmeter
        for i in trange(num):
            first_theta = par_lim[0][0] + (par_lim[0][1] - par_lim[0][0]) * np.random.random()
            second_theta = par_lim[1][0] + (par_lim[1][1] - par_lim[1][0]) * np.random.random()
            second_phi = par_lim[2][0] + (par_lim[2][1] - par_lim[2][0]) * np.random.random()
            info["theta_1"].append(first_theta)
            info["theta_2"].append(second_theta)
            info["phi_2"].append(second_phi)
            first_anchor = {
                "r":self.anchor_radius,
                "theta": first_theta,
                "phi":0
                }
            second_anchor = {
                "r":self.anchor_radius,
                "theta": second_theta,
                "phi":second_phi
                }
            info["chi2"].append(self(first_anchor,second_anchor))
        df = pd.DataFrame(info)
        return df
