#!/usr/bin/python3
"""
    Nonuniformity map for Tao
    ~~~~~~~~~~~~~~~~~~~~~~
    :author: Xu Hangkun (许杭锟)
    :copyright: © 2021 Xu Hangkun <xuhangkun@ihep.ac.cn>
    :license: MIT, see LICENSE for more details.
"""
from scipy import interpolate
import copy

class TaoNuMap:
    """ Nonuniformity map of Tao
    """
    def __init__(self,rawmapdata,kind="cubic"):
        """Inits TaoNonunMap
        Args:
            rawmapdata : nonuniformity map data
        """
        self.rawmapdata = rawmapdata
        self.interp_kind = kind
        self.interp_map = None
        self.initialize()
    
    def initialize(self):
        """build the interpolation object
        """
        self.radius = []
        self.theta = []
        self.value = []
        for item in self.rawmapdata:
            self.radius.append(item["r"])
            self.theta.append(item["theta"])
            self.value.append(item["nu_value"])
        if self.interp_kind == "cubic":
            self.interp_map = interpolate.CloughTocher2DInterpolator(list(zip(self.radius,self.theta)),self.value)
        else:
            self.interp_map = interpolate.LinearNDInterpolator(list(zip(self.radius,self.theta)),self.value)
    
    def __call__(self,radius_in,thetas_in):
        """
        Args:
            radius_in : np.array
            thetas_in : np.array with the same shape with radius_in
        
        Returns:
            non_uni_map_value : same shape with radius_in and thetas_in
        """
        radius = copy.deepcopy(radius_in)
        thetas  = copy.deepcopy(thetas_in)
        return self.interp_map(radius,thetas)