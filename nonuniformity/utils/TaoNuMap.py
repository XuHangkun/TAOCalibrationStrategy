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
from .tools import xyz2rthetaphi,rthetaphi2xyz
from tqdm import tqdm

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
    
    def reconstruct(self, events):
        """reconstruct event

        Args:
            events is a list of event, every event should be a dict
            eg. event = 
            {   
                "id":1, 
                "nhit": 4500, 
                "r": 300, 
                "theta":32 , 
                "phi": 32 , 
                "source":"positron",
                "edep":1.01
            }
        Return:
            Add a key "corrected_nhit" in every event
        """
        items = []
        for item in events:
            n_item = copy.deepcopy(item)
            n_item = self.reconstruct_event(n_item)
            items.append(n_item)
        return items
    
    def reconstruct_event(self, event):
        event["corrected_nhit"] = event["nhit"] / self(event["r"],event["theta"])
        return event


class DataForReconstruct:

    def __init__(self,data,source="positron"):
        """
        Args:
            data : TaoData
        """
        self.data = data
        self.source = source

    def get_normal_data(self, radius_cut = 650):
        self.data.SetBranchStatus(["*"],0)
        self.data.SetBranchStatus(
            ["fGdLSEdep","fGdLSEdepX","fGdLSEdepY","fGdLSEdepZ","fNSiPMHit","fPrimParticleKE"],1)
        events = []
        print("Read Data: %d samples. "%(self.data.GetEntries()))
        for i in tqdm(range(self.data.GetEntries())):
            self.data.GetEntry(i)
            x = self.data.GetAttr("fGdLSEdepX")
            y = self.data.GetAttr("fGdLSEdepY")
            z = self.data.GetAttr("fGdLSEdepZ")
            r,theta,phi = xyz2rthetaphi(x,y,z)
            if r > radius_cut:
                continue
            edep = self.data.GetAttr("fGdLSEdep")
            nhit = self.data.GetAttr("fNSiPMHit")
            if edep < 1.e-5 and nhit < 1:
                continue
            prim_particle_ke = self.data.GetAttr("fPrimParticleKE")
            item = {
                "id":i,
                "r":r,
                "theta":theta,
                "phi":phi,
                "nhit":nhit,
                "edep":edep,
                "source":self.source,
                "prim_particle_ke":sum(prim_particle_ke)
            }
            events.append(item)
        return events