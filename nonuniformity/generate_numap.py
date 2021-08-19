import argparse
import pandas as pd
from utils import config
from utils import generate_numap
import pickle

def generate_nnonuniformity_map():
    parser = argparse.ArgumentParser()
    parser.add_argument('--calibinfo_path', default = "../result/nonuniformity/ideal_nonuniformity_calibinfo.csv")
    parser.add_argument('--file_dir',default="/dybfs/users/xuhangkun/SimTAO/offline/change_data/nonuniformity/electron_1MeV")
    parser.add_argument('--no_symmetry', action="store_true")
    parser.add_argument('--sipm_dead_mode',default=None)
    parser.add_argument('--output',default=config["idealmap_path"])
    args = parser.parse_args()
    print(args)

    calib_info = pd.read_csv(args.calibinfo_path)
    ideal_map = generate_numap(
        calibration_data = calib_info,
        file_dir = args.file_dir,
        symmetry = not args.no_symmetry,
        sipm_dead_mode = args.sipm_dead_mode
    )
    file = open(args.output,"wb")
    pickle.dump(ideal_map,file)
    file.close()

if __name__ == "__main__":
    generate_nnonuniformity_map()