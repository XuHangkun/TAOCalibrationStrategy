from math import sqrt,asin,sin,acos,cos
import numpy as np


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

    return np.array([x,y,z])

def approx_equal(x,y,eps=1.e-3):
    if abs(y) < eps/10 and abs(x) < eps/10:
        return True
    if y*(1 + eps) >= x and y*(1 - eps) <= x:
        return True
    else:
        return False

def gamma_fitable(r,theta):
    if r > 750 and (theta < 8 or theta > (180 - 8)):
        return False
    else:
        return True

