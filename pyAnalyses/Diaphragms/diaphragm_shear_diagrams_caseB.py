
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:22:39 2019

@author: SMadhavan
"""
#import progressbar as prg
import excel_interface as ei
import plotter_caseB as pl

def mindex_df(df, index_by):
    df.set_index(index_by, inplace = True)
    return None

if __name__=="__main__":
    # =========================================================================
    # INPUTS - Please read the comments noted next to inputs.
    # =========================================================================
    # Note: Do not remove the 'r' in front of excel filepath. It indicates to 
    # the program that the filepath is in raw-string format. Just copy paste 
    # the filepath and place it within " ".
    excel_filepath = r"C:\Users\smadhavan\Documents\Python Scripts\diaphragm_shear_moment_diagrams\diaphragm_template_input_caseB.xlsx"
    sheet_name = 'Diaphragm Shear Summary' # Name of the excel tab
    start_row_no = 2  # This is the row number in excel (including header row)
    end_row_no = 68   # Row number of the last data point
    start_col_no = "I"  # Column label of first column of data
    end_col_no = "O"    # Column label of last column of data
    fig_folder = "Diaphragm Diagrams Y"   # This folder has to exist with this 
                                          # name, where your script lives
    index_by = ['Level']    # Caution! This is used to group output
                            # Modify only if you know what you're doing
    # Run the script for each direction by changing start_col_no, end_col_no and fig_folder
    # =========================================================================
    # =========================================================================
    
    data_range = ei.get_excel_range(start_row_no, end_row_no, start_col_no, end_col_no)
    df = ei.get_df_from_input(excel_filepath, sheet_name, data_range)
    mindex_df(df, index_by)
    dfg = df.groupby(level = [0])
    #bar = prg.ProgressBar(max_value=len(dfg))
    progress_counter = 0
    for story, group in dfg:
        pl.plot_shear_diagram(story, group, 
                                  fig_folderpath = fig_folder, 
                                  save_fig = True, close_fig = True)
        pl.plot_moment_diagram(story, group, 
                                  fig_folderpath = fig_folder, 
                                  save_fig = True, close_fig = True)
        progress_counter +=1
        #bar.update(progress_counter)
    
    print("\n Success!")


