import pickle
from math import sqrt,asin,sin,acos,cos
import numpy as np
import yaml

def read_pickle_data(file_path):
    file  = open(file_path,"rb")
    data = pickle.load(file)
    file.close()
    return data

def save_pickle_data(data,file_path):
    file  = open(file_path,"wb")
    pickle.dump(data,file)
    file.close()

def read_yaml_data(file_path):
    f  = open(file_path,"r")
    data = yaml.safe_load(f)
    f.close()
    return data

def save_yaml_data(data,file_path):
    file  = open(file_path,"w")
    yaml.dump(data = data,stream = file)
    file.close()

def xyz2rthetaphi(x,y,z):
    """convert x,y,z to radiu,theta,phi
    """
    radius = sqrt(x*x + y*y + z*z)
    if radius < 1.e-3:
        radius = 1.e-3
    theta = acos(z/radius)*180./3.1415926
    if x < 1.e-5 and y < 1.e-5:
        phi = 0
    else:
        phi = acos(x/sqrt(x*x + y*y))*180./3.1415926
    if y < 0:
        phi = 360 - phi
    return np.array([radius,theta,phi])

def rthetaphi2xyz(radius,theta,phi):
    """convert radius,theta,phi to x,y,z
    """
    theta *= 3.1415926/180
    phi *= 3.1415926/180
    z = radius * cos(theta)
    x = radius * sin(theta) * cos(phi)
    y = radius * sin(theta) * sin(phi)
