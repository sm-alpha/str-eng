# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:47:25 2019

@author: SMadhavan
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar


def compute_beta1(f_c_psi):
    if 2500 <= f_c_psi <= 4000:
        return 0.85
    elif 4000 < f_c_psi < 8000:
        return round(0.85-(0.05*(f_c_psi - 4000)/1000),2)
    else:
        return 0.65


def compute_plastic_stress(FC, FY, c, beta_1, d_tos, d_steel, b_f, b_w, t_f, d_conf, b_conf):
    #Assumptions include that steel is wide flange and is symmetric
    #Checks
    if d_steel > d_conf:
        print("Error! Depth of confined portion of concrete beam "
              "should at least be equal to steel beam depth.")
        return None
    if d_steel + d_tos > d_conf:
        print("Error! Depth to top of steel + depth of steel beam "
              "should be less than or equal to depth of confined portion of concrete beam.")
        return None
    if b_conf <= b_w:
        print("Error! Your concrete confined width is smaller than thickness of web of steel. "
              "Get a cup of coffee and check your input please.")
        return None
    if b_f > b_conf:
        b_f = b_conf
        """
        print("Flange width of steel beam exceeds the confined concrete width. "
              "Flange width has been terminated to be equal to width of confined concrete. "
              "Check input if this insn't the intent. Alternatively, "
              "incorporate the terminated flange width in your detail.")
        """
    if c > (d_conf/2):
        print("Error! c value greater than half the depth of confined portion of concrete beam. "
              "Equilibrium cannot be satisfied under this condition. Please check input.")
        return None
    
    a = beta_1*c
    if a <= 0:
        print("Error! 'a' value less than or equal to 0. Please check input!")
        return None
    
    A1cc = d_tos*b_conf
    y1cc = d_tos/2
    
    if a <= d_tos:
        A2cc = 0
        y2cc = 0
        A3cc = 0
        y3cc = 0
    elif d_tos < a <= (d_tos + t_f):
        A2cc = (b_conf-b_f)*(a - d_tos)
        y2cc = d_tos + 0.5*(a - d_tos)
        A3cc = 0
        y3cc = 0
    else:
        A2cc = (b_conf-b_f)*t_f
        y2cc = d_tos + 0.5*t_f
        A3cc = (b_conf-b_w)*(a-d_tos-t_f)
        y3cc = 0.5*(d_tos + t_f + a)
        
        
    if c <= d_tos:
        A1sc = 0
        y1sc = 0
        A2sc = 0
        y2sc = 0
        A3st = t_f*b_f
        y3st = d_tos + 0.5*t_f
        A4st = (d_steel - 2*t_f)*b_w
        y4st = d_tos + 0.5*(d_steel)
    elif d_tos < c <= (d_tos + t_f):
        A1sc = (c - d_tos)*b_f
        y1sc = 0.5*(c + d_tos)
        A2sc = 0
        y2sc = 0
        A3st = (d_tos + t_f - c)*b_f
        y3st = 0.5*(c + d_tos + t_f)
        A4st = (d_steel - 2*t_f)*b_w
        y4st = d_tos + 0.5*(d_steel)
    else:
        A1sc = t_f*b_f
        y1sc = d_tos + 0.5*t_f
        A2sc = (c-d_tos-t_f)*b_w
        y2sc = 0.5*(d_tos + t_f + c)
        A3st = 0
        y3st = 0
        A4st = (d_tos+d_steel-c-t_f)*b_w
        y4st = 0.5*(d_tos + d_steel + c - t_f)

    
    A5st = t_f*b_f
    y5st = d_tos + d_steel - 0.5*t_f   
    
    A = [A1cc, A2cc, A3cc, A1sc, A2sc, A3st, A4st, A5st]
    y = [y1cc, y2cc, y3cc, y1sc, y2sc, y3st, y4st, y5st]
    y_from_c = [round(i-c,2) for i in y]
    sigma = [-FC]*3+[-FY]*2+[FY]*3
    force = [round(i*j) for i,j in zip(sigma, A)]
    delta = sum(force)
    return delta, force, y_from_c


def optimize(delta_series, c_series):
    
    delta, F, y = compute_plastic_stress(FC, FY, 
                                            c, beta_1, d_tos, d_steel, 
                                            b_f, b_w, t_f, d_conf, 
                                            b_conf)
    delta_series.append(delta)
    c_series.append(c)
    i = 1
    c_iter = iterate(c, delta, np.inf)
    while c_iter != c_series[i-1]:
        delta, F, y = compute_plastic_stress(FC, FY, 
                                                c_iter, beta_1, d_tos, d_steel, 
                                                b_f, b_w, t_f, d_conf, 
                                                b_conf)
        delta_series.append(delta)
        c_series.append(c_iter)
        c_iter = iterate(c_iter, delta, delta_series[i-1])
        i+=1
    
    return delta, F, y
        
def foo(c):
    delta = compute_plastic_stress(FC, FY, 
                                    c, beta_1, d_tos, d_steel, 
                                    b_f, b_w, t_f, d_conf, 
                                    b_conf)[0]
    return abs(delta)
    
def iterate(c, delta, delta_prev, step = 0.2, threshold = 2):
    assert(c > 0)
    if abs(delta) > abs(delta_prev):
        print("Delta is increasing. Something is off!")
        return c
    if abs(delta) <= threshold:
        return c
    else:
        return round(c - step,2)

def moment_resisted(force, distance):
    M = np.inner(force,distance)
    return round(M)

if __name__ == "__main__":
    """
    #Concrete Properties
    b_conf = 24 #inches; width of confined portion of concrete beam
    d_conf = 36 #inches; depth of confined portion of concrete beam
    d_tos = 4.85 #inches; depth to top of steel beam
    
    #Steel Properties
    b_f = 13.2
    t_f = 1.89
    d_steel = 26.3
    b_w = 1.04
    
    f_c = 6
    FC = 0.85*f_c
    FY = 50
    beta_1 = 0.75
    """
    #Concrete Properties
    b_conf = 13.75 #inches; width of confined portion of concrete beam
    d_conf = 15.75 #inches; depth of confined portion of concrete beam
    d_tos = 0.625 #inches; depth to top of steel beam
    
    #Steel Properties
    b_f = 14.7
    t_f = 0.94
    d_steel = 14.5
    b_w = 0.59
    
    f_c = 8
    FC = 0.85*f_c
    FY = 50
    beta_1 = 0.65
    
    #c = 4.65

    res = minimize_scalar(foo, bounds=(d_tos, d_tos+0.5*d_steel), method='bounded')
    c = res.x
    print("c (inches) = ",round(c,3))
    """
    delta_series = []
    c_series = []
    c = np.linspace(d_tos, d_tos+0.5*d_steel, 200)
    #c = 13
    #delta, F, y_na = optimize(delta_series, c_series)
    for c_i in c:
        delta = compute_plastic_stress(FC, FY, 
                                            c_i, beta_1, d_tos, d_steel, 
                                            b_f, b_w, t_f, d_conf, 
                                            b_conf)[0]
        delta_series.append(abs(delta))
    
    plt.plot(c, delta_series)
    plt.grid(True)
    plt.xlabel("c (inches) measured from top of beam")
    plt.ylabel("unbalanced force (kips)")
    print(c_series)
    """
    
    delta, F, y_na = compute_plastic_stress(FC, FY, 
                                        c, beta_1, d_tos, d_steel, 
                                        b_f, b_w, t_f, d_conf, 
                                        b_conf)
    Mp = moment_resisted(np.array(F), np.array(y_na))
    
    print("Sum of compressive forces (kips) = ",sum(F[:5]))
    print("Sum of tensile forces (kips) = ",sum(F[-3:]))
    print("Unbalanced force (kips) = ", delta)
    print("Mp (kip-in) = ", Mp)