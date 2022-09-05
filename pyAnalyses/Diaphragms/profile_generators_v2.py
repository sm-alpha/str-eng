# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:18:53 2020

@author: SMadhavan
"""
import numpy as np

def get_shear_profile(x_tot, R):
    x_tot = np.array(x_tot)
    R = np.array(R)
    L = x_tot[-1]
    w = sum(R)/L
    SF_dist = -w*x_tot
    R_tot = np.cumsum(R)
    bottom_points = R_tot + SF_dist
    top_points = np.pad(SF_dist[1:]+R_tot[:-1], (1,0))
    x = np.repeat(x_tot,2)
    y = -np.insert(top_points, range(1, len(bottom_points)+1),bottom_points)
    return (x, y)

def get_max_value(y):
    max_value = round(max(y, key = abs))
    return max_value

def conc_moment(xi, xarr, Rarr):
    mask = xarr < xi
    xf = xarr[mask]
    Rf = Rarr[mask]
    x_delta = xi - xf
    conc_moment_arr = Rf*x_delta
    conc_BM = sum(conc_moment_arr)
    return conc_BM

def dist_moment(xi, w):
    dist_BM = 0.5*w*(xi**2)
    return dist_BM

def get_moment_profile(x_tot, R, step = 0.5):
    x_tot = np.array(x_tot)
    R = np.array(R)
    L = x_tot[-1]
    w = sum(R)/L
    x_detail = np.arange(x_tot[0], x_tot[-1]+step, step)
    BM_detail = -np.array([conc_moment(xi, x_tot, R) - dist_moment(xi, w) for xi in x_detail])
    correcting_force = -BM_detail[-1]/x_detail[-1]
    C_detail = correcting_force*x_detail
    CM_detail = C_detail + BM_detail
    return x_detail, BM_detail, C_detail, CM_detail