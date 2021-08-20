# **Nonuniformity calibration**

## **Set the enviroment**
```bash
$ source setup.sh
```

## **Ideal nonuniformity map**
* generate ideal map calibration info first
```shell
$ python3 calibinfo/create_idealmap_info.py
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