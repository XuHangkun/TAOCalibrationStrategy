import argparse
import pickle
from utils import config
from utils import TaoNuMap, generate_pointcalib_info
from utils import generate_numap

def create_idealpointcalib():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--ideal_numap_path',default = config["idealmap_path"])
    parser.add_argument('--anchor_pars',default = [102.5,155.2,151.7])
    parser.add_argument('--calib_sim_dir',default = "/dybfs/users/xuhangkun/SimTAO/offline/change_data/nonuniformity/gamma")
    parser.add_argument('--sipm_dead_mode',default=None)
    parser.add_argument('--sipm_dead_seed',default=7,type=int)
    parser.add_argument('--output',default="../result/nonuniformity/point_calib_map.pkl")
    parser.add_argument('--calib_info_output',default="../result/nonuniformity/point_calib_info.csv")
    args = parser.parse_args()
    print(args)

    # load ideal non-uniformity map
    file = open(args.ideal_numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind="cubic")
    file.close()

    # get point calib info
    first_anchor = {"r":870,"theta":args.anchor_pars[0],"phi":0}
    second_anchor = {"r":870,"theta":args.anchor_pars[1],"phi":args.anchor_pars[2]}
    calibinfo = generate_pointcalib_info(tao_nu_map,first_anchor,second_anchor)
    calibinfo.to_csv(args.calib_info_output)

    # generate nonuniformity calibrated by gamma sources
    point_calib_map_info = generate_numap(calibinfo,
        file_dir = args.calib_sim_dir,
        symmetry = True,
        sipm_dead_mode = args.sipm_dead_mode,
        sipm_dead_seed = args.sipm_dead_seed
        )

    # save the map
    file = open(args.output,"wb")
    pickle.dump(point_calib_map_info,file)
    file.close()

if __name__ == "__main__":
    create_idealpointcalib()
