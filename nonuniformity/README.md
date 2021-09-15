# **Nonuniformity calibration**

## **Set the enviroment**
```bash
$ source setup.sh
```

## **Ideal nonuniformity map**
* generate ideal map calibration info first
```shell
$ python3 calibinfo/create_idealmap_info.py --no_symmetry
```
* generate the nonuniformity map
```shell
$ python3 generate_numap.py
```
* draw the nonuniformity map
```shell
$ python draw/draw_nonuniformity_map.py
```

## **Optimize the CLS parameters**
* optimize anchor position
```shell
$ python optimize_anchor_positions.py
```
* draw the result
```shell
$ python draw/draw_numap_byanchor.py
```
* Select the ideal calib point and generate the ideal_point_calib info
```shell
$ 
```

## **Reconstruction**
```shell
$ # Reconstruct by ideal map
$ python reconstruct_IBD.py
$ # reconstruct by calib map
$ python reconstruct_IBD.py --numap_path ../result/nonuniformity/point_calib_map.pkl --filter_points --output ../result/nonuniformity/IBD_reconstructed_by_calib_numap.pkl
$ # reconstruct by calib map, consider vertex smear
$ python reconstruct_IBD.py --numap_path ../result/nonuniformity/point_calib_map.pkl --filter_points --output ../result/nonuniformity/IBD_reconstructed_by_calib_numap_vertexsmear.pkl --vertex_smear 50
```