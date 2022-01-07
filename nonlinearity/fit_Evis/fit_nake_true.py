from utils import TaoNuMap, DataForReconstruct
from utils import read_yaml_data, save_yaml_data
from utils import read_pickle_data, save_pickle_data
from TaoDataAPI import TAOData
import numpy as np
import matplotlib.pyplot as plt

def fit_nake_data(
        source,
        energy,
        file_path
        ):
    data = TAOData([file_path])
    data_rec = DataForReconstruct(data,energy,source)
    events = data_rec.get_normal_data()

    tao_nu = TaoNuMap(read_pickle_data("./input/point_calib_map.pkl"))
    recon_events = tao_nu.reconstruct(events)

    nake_evis = []
    corrected_nake_evis = []
    for item in recon_events:
        nake_evis.append(item["nhit"])
        corrected_nake_evis.append(item["corrected_nhit"])
    # We decide to use corrected data
    info = {
            "nake_evis" : float(np.mean(corrected_nake_evis)),
            "nake_evis_e": float(np.std(corrected_nake_evis)/np.sqrt(len(corrected_nake_evis))),
            "corrected_nake_evis" : float(np.mean(corrected_nake_evis)),
            "corrected_nake_evis_e": float(np.std(corrected_nake_evis)/np.sqrt(len(corrected_nake_evis)))
            }
    print(source)
    print(info)
    return info

def plot_evis(config):
    energies = []
    corr_ratio = []
    for k,v in config.items():
        energies.append(v["total_gamma_e"])
        corr_ratio.append(v["corrected_nake_evis"]/v["nake_evis"])
    plt.plot(energies, corr_ratio)
    plt.show()

if __name__ == "__main__":
    config = read_yaml_data("./input/nake_source_info.yaml")
    for key,item in config.items():
        fit_info = fit_nake_data(key, item["total_gamma_e"], item["file_path"])
        for k,v in fit_info.items():
            item[k] = v
    print(config)
    save_yaml_data(config,"./input/fit/nake_true_info.yaml")
    plot_evis(config)
