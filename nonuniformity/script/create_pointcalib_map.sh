#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:/dybfs/users/xuhangkun/SOFTWARE/VSCode/.local/lib/python3.6/site-packages
source setup.sh

sipm_dead_seed=${1}
python3 create_pointcalib_map.py \
--sipm_dead_mode uni \
--sipm_dead_seed ${sipm_dead_seed} \
--output ../result/nonuniformity/map/point_calib_map_sipmdead_seed${sipm_dead_seed}.pkl \
--calib_info_output ../result/nonuniformity/map/point_calib_info_sipmdead_seed${sipm_dead_seed}.csv
