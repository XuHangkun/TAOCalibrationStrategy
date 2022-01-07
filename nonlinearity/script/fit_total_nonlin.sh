#!/bin/bash
# export PYTHONPATH=${PYTHONPATH}:/dybfs/users/xuhangkun/SOFTWARE/VSCode/.local/lib/python3.6/site-packages
source setup.sh

index=${1}
python3 fit_total_nonlin.py --fit_mode sigma_band \
--output ../result/nonlinearity/fit/fit_total_nonlin_sigmaband_v${index}.pkl
