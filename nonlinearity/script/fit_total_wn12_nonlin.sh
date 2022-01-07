#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:/dybfs/users/xuhangkun/SOFTWARE/VSCode/.local/lib/python3.6/site-packages
source setup.sh

index=${1}
python3 fit_total_wn12_nonlin.py --fit_mode sigma_band \
--output ../result/nonlinearity/fitwn12/fit_total_nonlin_sigmaband_v${index}.pkl
