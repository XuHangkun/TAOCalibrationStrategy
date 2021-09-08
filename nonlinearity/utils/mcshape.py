from math import exp,pow,sqrt,sin,cos
import pandas as pd
import ROOT

class MCShape:

    def __init__(self,
            source,
            energy,
            eleak_temp
        ):
        """
        Args:
            source : name of radioactive source, eg: Cs137
            energy : energy of radioactive, eg: 0.661
            eleak_temp : THist, eleak template
        """
        self.source = source
        self.energy = energy
        self.eleak_temp = eleak_temp
        self.eleak_spec = ELeakSpec(source,energy,eleak_temp)

    def __call__(self,x,par):
        """
        par:
            par[0]: amplitude for gaus
            par[1]: peak value
            par[2]: 100%* relative sigma
            par[3]: relative amplitude for energy leak spectrum
        """
        gaus_par = [par[0],par[1],par[2]]
        gaus = Gaus(x,gaus_par)

        eleak_par = [par[0]*par[3],par[1]]
        eleak_value = self.eleak_spec(x,eleak_par)

        return gaus + eleak_value

    def leak_energy_spec(self,x,par):
        eleak_par = [par[0]*par[3],par[1]]
        eleak_value = self.eleak_spec(x,eleak_par)
        return eleak_value

    def full_energy_spec(self,x,par):
        gaus_par = [par[0],par[1],par[2]]
        gaus = Gaus(x,gaus_par)
        return gaus

class MulMCShape:

    def __init__(self,
        sources,
        energies,
        eleak_temps
        ):
        """
        Args:
            sources : names of radioactive source, eg: Cs137
            energies : energies of radioactive, eg: 0.661
            eleak_temps : THists, eleak template
        """
        assert len(sources) == len(energies)
        assert len(sources) == len(eleak_temps)
        self.sources = sources
        self.energies = energies
        self.eleak_temps = eleak_temps
        self.mcshapes = [MCShape(s,e,tmp) for s,e,tmp in zip(sources,energies,eleak_temps)]

    def __call__(self,x,par):
        """
        Args:
            par : lenght of par must be 4*len(sources)
        """
        value = 0
        for index,shape in enumerate(self.mcshapes):
            pars = [par[i] for i in range(4*index,4*index + 4)]
            value += shape(x,pars)
        return value

    def source_spec(self,source,x,par):
        index = self.sources.index(source)
        pars = [par[i] for i in range(4*index,4*index + 4)]
        value = self.mcshapes[index](x,pars)
        return value

class ELeakSpec:

    def __init__(self,
            source,
            energy,
            eleak_temp
        ):
        """
        Args:
            source : name of radioactive source, eg: Cs137
            energy : energy of radioactive, eg: 0.661
            eleak_temp : TGraph, eleak template
        """
        self.source = source
        self.energy = energy
        self.eleak_temp = eleak_temp

    def __call__(self,x,par):
        """
        par:
            par[0]: amplitude
            par[1]: peak value of full energy
        """
        escale = par[1]/self.energy
        return par[0]*self.eleak_temp.Eval(x[0]*1.0/escale)

    @staticmethod
    def create_eleak_temp_by_csv(eleak_file):
        df_eleak = pd.read_csv(eleak_file)
        eleak_temp = ROOT.TGraph(len(df_eleak["energy"].to_numpy()),df_eleak["energy"].to_numpy(),df_eleak["value"].to_numpy())
        return eleak_temp

def Gaus(x,par):
    # gaus part
    gaus = par[0]*exp(-0.5*pow((x[0]-par[1])/(par[1]*par[2]*0.01),2))
    return gaus
