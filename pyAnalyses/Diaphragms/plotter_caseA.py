# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 19:09:02 2021

@author: SMadhavan
"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'monospace'
rcParams['font.monospace'] = ['Calibri']
rcParams['font.size'] = 10
rcParams['pdf.fonttype'] = 42

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