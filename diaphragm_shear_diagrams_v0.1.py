
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:22:39 2019

@author: SMadhavan
"""
#import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'monospace'
rcParams['font.monospace'] = ['Calibri']
rcParams['font.size'] = 10
rcParams['pdf.fonttype'] = 42
from matplotlib.backends.backend_pdf import PdfPages

def get_shear_profile(x_prev, R):
    #R = np.array([R])
    print("Total loading (kip) : ", sum(R))   
    x_tot = np.cumsum(x_prev)
    #x_tot = [0,34,74,144,172.5]
    L = x_tot[-1]
    print("Total length  (ft)  : ", L)
    w = sum(R)/L
    print("Distributed loading (kip/ft) : ", round(w))
    #w = 52.1739130434783 #klf
    SF_dist = -w*x_tot
    R_tot = np.cumsum(R)
    bottom_points = R_tot + SF_dist
    top_points = SF_dist[1:-1]+R_tot[:-2]
    x = np.repeat(x_tot,2)[1:-1]
    y = np.insert(bottom_points, range(1,len(top_points)+1), top_points)
    max_shear = round(max(y, key = abs))
    print("Max shear (kips) : ", max_shear)
    return (x, y, x_tot, w, max_shear)

def plot_shear_diagram(x, y):
    fig = plt.figure("Shear Diagram")
    plt.plot(x,y, marker = 'o', markersize = 3)
    plt.grid(True, alpha = 0.3)
    for xi, yi in zip(x, y):
        label = "{:.0f}".format(yi)
        plt.annotate(label, (xi, yi), textcoords="offset points", xytext=(12,0), ha = 'center')
    plt.axhline(y = 0, color = 'k', alpha = 0.3)
    plt.xlabel("Length (ft)")
    plt.ylabel("Shear force (kip)")
    plt.title("Diaphragm Shear Diagram")
    plt.tight_layout()
    return fig

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

def get_moment_profile(x_tot, R, w, step = 0.5):
    x_detail = np.arange(x_tot[0], x_tot[-1]+step, step)
    BM_detail = [conc_moment(xi, x_tot, R) - dist_moment(xi, w) for xi in x_detail]
    correcting_force = -BM_detail[-1]/x_detail[-1]
    C_detail = correcting_force*x_detail
    CM_detail = C_detail + BM_detail
    return x_detail, BM_detail, C_detail, CM_detail

def plot_moment_diagram(x_detail, BM_detail, C_detail, CM_detail):
    fig = plt.figure("Moment Diagram")
    plt.plot(x_detail, BM_detail, x_detail, C_detail, x_detail, CM_detail)
    plt.grid(True, alpha = 0.3)
    plt.axhline(y = 0, color = 'k', alpha = 0.3)
    plt.xlabel("Length (ft)")
    plt.ylabel("Bending Moment (kip-ft)")
    plt.title("Diaphragm Moment Diagram")
    plt.legend(["Uncorrected Moment","Correction","Corrected Moment"])
    plt.tight_layout()
    return fig

def get_plots(x_prev, R, BM_plot_step):
    (x, y, x_tot, w, max_shear) = get_shear_profile(x_prev, R)
    fig1 = plot_shear_diagram(x, y)
    (x_d, BM_d, C_d, CM_d) = get_moment_profile(x_tot, R, w, BM_plot_step)
    fig2 = plot_moment_diagram(x_d, BM_d, C_d, CM_d)
    return max_shear
    

if __name__=="__main__":
    
    BM_plot_step = 0.5 #optional
    x_prev = np.array([0, 9.75, 17, 7, 17, 25]) #length to reaction points in beam idealization. Sum of the lengths gives the total diaphragm span
    L_perp = 172.5 #Diaphragm span in perpendicular direction
    R = np.array([0,3100,500,3500,4500,0]) #The forces at each of the support points
    max_shear = get_plots(x_prev, R, BM_plot_step)
    Vu = abs(round(max_shear/L_perp, 1))
    print("Vu (kips/ft) : ",Vu)

