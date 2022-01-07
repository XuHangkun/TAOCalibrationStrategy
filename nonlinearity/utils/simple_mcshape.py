from math import exp,pow,sqrt,sin,cos,erfc
import pandas as pd
import ROOT

class SimpleMCShape:

    def __init__(self):
        pass

    def __call__(self,x,par):
        """
        par:
            par[0]: amplitude for gaus
            par[1]: peak value
            par[2]: 100%* relative sigma
            par[3]: relative amplitude for energy leak spectrum
        """
        return self.gaus(x,par) + self.leak_energy_spec(x,par)

    def gaus(self,x,par):
        return par[0]*exp(-1./2*((x[0]-par[1])/par[2])**2)

    def leak_energy_spec(self,x,par):
        return par[3]*erfc((x[0]-par[1])/sqrt(2)/par[2])

class SimpleNHMCShape(SimpleMCShape):

    def leak_energy_spec(self,x,par):
        return par[3]*erfc((x[0]-par[1])/sqrt(2)/par[2]) + par[4]

class MulSimpleMCShape:

    def __init__(self, number):
        self.number = number
        self.mcshape = SimpleMCShape()

    def __call__(self,x,par):
        """
        Args:
            par : lenght of par must be 4*len(sources)
        """
        value = 0
        for index in range(self.number):
            pars = [par[i] for i in range(4*index,4*index + 4)]
            value += self.mcshape(x,pars)
        return value

    def source_spec(self,x,par):
        return self.mcshape(x,par)

    def source_leak_spec(self,x,par):
        return self.mcshape.leak_energy_spec(x,par)

