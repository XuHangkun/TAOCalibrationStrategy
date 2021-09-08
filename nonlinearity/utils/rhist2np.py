import numpy as np

def rhist2np(hist):
    x = np.zeros(hist.GetNbinsX())
    hist.GetXaxis().GetCenter(x)
    y = np.asarray(hist)[1:-1]
    return x,y
