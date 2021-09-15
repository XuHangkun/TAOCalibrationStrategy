#!/bin/bash
sipm_dead_mode=${1}
python draw/draw_resolution.py --uniform_inputs \
../result/nonuniformity/IBD_uniform_reconstructed_by_calib_numap_sipmdead_${sipm_dead_mode}.pkl \
--uniform_labels ${sipm_dead_mode} \
--central_input ../result/nonuniformity/IBD_central_reconstructed_by_calib_numap_sipmdead_${sipm_dead_mode}.pkl \
--output_resolution ../result/nonuniformity/fig/IBD_reconstructed_sipmdead_${sipm_dead_mode}_resolution.eps \
--output_bias ../result/nonuniformity/fig/IBD_reconstructed_sipmdead_${sipm_dead_mode}_bias.eps
