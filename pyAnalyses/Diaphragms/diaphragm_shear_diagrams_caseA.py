
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:22:39 2019

@author: SMadhavan
"""
import pandas as pd
import plotter_caseA as pl
import profile_generators_v2 as pg
    
def get_plots(lengths, forces, BM_plot_step = 0.5):
    (x, y) = pg.get_shear_profile(lengths, forces)
    pl.plot_shear_diagram(x, y)
    (x_d, BM_d, C_d, CM_d) = pg.get_moment_profile(lengths, forces, BM_plot_step)
    pl.plot_moment_diagram(x_d, BM_d, C_d, CM_d)
    return None
    
if __name__=="__main__":
    # =========================================================================
    # INPUTS - Please read the comments
    # =========================================================================
    
    # OPTION 1 - Uncomment the lengths and forces list below and enter values manually
    # Easy for a simple diaphragm with few force resisting lines
    
    #lengths = [0, 25, 50, 75] #ft
    #forces = [40, 30, 30, 40] #kip
    
    # OPTION 2 - Using an excel file similar to template
    # The sheet has first column as lengths and second column as forces
    # Note: Do not remove the 'r' in front of excel filepath. It indicates to 
    # the program that the filepath is in raw-string format. Just copy paste 
    # the filepath and place it within double quotes " ".
    
    filepath = r"C:\Users\smadhavan\Documents\Python Scripts\diaphragm_shear_moment_diagrams\diaphragm_template_input_caseA.xlsx"
    # =========================================================================
    # You can save the output figures in whatever file format you like
    # =========================================================================
    data = pd.read_excel(filepath)
    lengths, forces = data[data.columns[0]], data[data.columns[1]]
    get_plots(lengths, forces)
    


