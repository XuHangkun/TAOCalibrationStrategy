#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:/dybfs/users/xuhangkun/SOFTWARE/VSCode/.local/lib/python3.6/site-packages
source setup.sh

sipm_dead_mode=${1}
python3 reconstruct_IBD.py \
--numap_path ../result/nonuniformity/point_calib_map_sipmdead_${sipm_dead_mode}.pkl \
--filter_points --vertex_smear 50 --sipm_dead_mode ${sipm_dead_mode} \
--IBD_dir /dybfs/users/xuhangkun/SimTAO/offline/change_data/positron \
--output ../result/nonuniformity/IBD_central_reconstructed_by_calib_numap_sipmdead_${sipm_dead_mode}.pkl
