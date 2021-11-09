# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 22:55:44 2021

@author: srikr
"""

def get_As(phi, fc, fy, b, d, Mu):
    
    x = 0.85*fc*b/fy
    y = 2*x/(phi*fy)
    As = x*d-((x*d)**2 - Mu*y)**0.5
    return x, y, As

if __name__=="__main__":
    phi = 0.9
    fc = 6000
    fy = 60000
    b = 12
    d = 42
    Mu = 100000
    x, y, As = get_As(phi, fc, fy, b, d, Mu)
    print(x, x**2, y*1e3)
    print(round(As,3))