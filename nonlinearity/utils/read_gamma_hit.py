from TaoDataAPI import TAOData
from .config import config
import ROOT
from tqdm import tqdm

def read_gamma_hit(source,files,energy,num=50000,xrange=None,nbin=300):
    """
    create generate energy spectrum
    pars:
        files: files of radioactice source calibration data
        energy: energy for radioactive source
        num: events which own gammas
        range: range of histogram
    returns:
        hist: energy of histogram
    """
    xrange = xrange
    if not xrange:
        xrange = (0,float(1.2*energy))
    data = TAOData(files)
    data.SetBranchStatus(["*"],0)
    data.SetBranchStatus(["fPrimParticlePDG","fGdLSEdep","fNSiPMHit"],1)
    num_entry = data.GetEntries()
    gamma_count=0
    index=0
    hit_h = ROOT.TH1F("%s_energy_spec"%(source),"spectrum of energy",nbin,xrange[0],xrange[1])
    full_hit_h = ROOT.TH1F("%s_full_energy_spec"%(source),"spectrum of energy",nbin,xrange[0],xrange[1])
    while True:
        data.GetEntry(index%num_entry)
        pdg_code = data.GetAttr("fPrimParticlePDG")
        if (-11 in pdg_code) or (22 in pdg_code):
            gamma_count += 1
        else:
            gamma_count += 1
        hit_sum = data.GetAttr("fNSiPMHit")
        edep = data.GetAttr("fGdLSEdep")
        hit_h.Fill(hit_sum/config["energy_scale"])
        if (edep > energy*0.9999) and (edep < energy*1.0001):
            full_hit_h.Fill(hit_sum/config["energy_scale"])
        index += 1
        if gamma_count%300000 == 0:
            print("Read %d events."%(gamma_count))
        if gamma_count>=num:
            print(gamma_count," Reached!")
            break
    return hit_h, full_hit_h
