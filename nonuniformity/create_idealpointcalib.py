import argparse
import pickle
from utils import config
from utils import TaoNuMap,generate_idealpointcalib_info

def create_idealpointcalib():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--ideal_numap_path',default = config["idealmap_path"])
    parser.add_argument('--anchor_pars',default = [102.5,155.2,151.7])
    parser.add_argument('--output',default="../result/nonuniformity/ideal_point_calib_info.pkl")
    args = parser.parse_args()
    print(args)

    file = open(args.ideal_numap_path,"rb")
    mapinfo = pickle.load(file)
    tao_nu_map = TaoNuMap(mapinfo,kind="linear")
    file.close()

    # anchors define
    first_anchor = {"r":870,"theta":args.anchor_pars[0],"phi":0}
    second_anchor = {"r":870,"theta":args.anchor_pars[1],"phi":args.anchor_pars[2]}
    calibinfo = generate_idealpointcalib_info(tao_nu_map,first_anchor,second_anchor)
    file = open(args.output,"wb")
    pickle.dump(calibinfo,file)
    file.close()

if __name__ == "__main__":
    create_idealpointcalib()