# Non-linearity calibration

## Get systematic biases and uncertainties
### Fitting bias
- Fit each ratioactive source and get the fitting bias
```shell
$ # default save the fitting fig. to ../result/nonlinearity/fig/SOURCE_spec_fit.eps
$ # you can choose to change the fit_bias, uncertainty and nPE in the ra_fit_info.yaml or not!!!
$ # Neutron is different, it's full absorption energy should be 2.2259 here
$ # Please check that you are done the right thing here!
$ python fit_Evis/simple_fit_combine_source.py  
$ python fit_Evis/simple_fit_single_gamma.py  
$ python fit_Evis/simple_fit_nH.py
```
- Write fitting biases to ./input/fit/ra_fit_info.yaml

### Shadowing bias
- Get the Evis of full-absorption peak of naked sources and enclosured sources, then calculate the shadowing bias
- Write shadowing bais to ./input/fit/shadowing_info.yaml

### Generate Nake True
- generate the Evis of full absorption peak
```shell
$ python fit_Evis/fit_nake_true.py
```
- Write fitting biases to ./input/fit/nake_true_info.yaml

## Fit the gamma data and B12 data
### Input
- ./input/fit/ra_fit_info.yaml : fitting bias
- ./input/fit/shadowing_info.yaml : shadowing bias
- ./input/fit/nake_true_info.yaml : nake true
- ./input/fit/continue_spectrum_hits.pkl : hits of 12B
- ./input/fit/continue_spectrum.root : edep spectrum of 12B
- ./input/fit/true_electron_nonlin.pkl : true electron non-linearity

### Fitting
```shell
$ # fit non-linearity with/without 12B data
$ python fit_gamma_nonlin.py 
$ python fit_total_nonlin.py
```

### Show
```shell
$ python draw/draw_b12_fitting.py 
$ python draw/draw_gamma_fitting.py 
$ python draw/draw_electron_nonlin.py 
```
