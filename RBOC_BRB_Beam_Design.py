# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:40:25 2020

@author: SMadhavan
"""

import xlwings as xw

# =============================================================================
# INPUTS
# =============================================================================
wb_out = xw.Book("RBOC_BRBF_Beam_Forces_SW Tower.xlsx")
summary_sheet_name = 'Summary'
start_row_no = 6
end_row_no = 115
load_pairs_column_no = [("H","I"),("J","K"),("L","M")]
beam_size_column_no = "G"
beam_length_column_no = "F"
DCR_output_cols = ["N", "O","P"]
load_cases = 3

wb_design = xw.Book("BRB Beam Designs - RBOC.xlsx")
design_sheet_name = 'Beam Design'
LenLoc = "P19"
PuLoc = "P21"
MuLoc = "P38"
MemLoc = "Q7"
DcrOut =  "Q63"

# =============================================================================
# Preprocessing to get the values from the ranges specified
# =============================================================================

def get_load_pair_ranges(start_row_no, end_row_no, load_pairs_column_no):
    load_pair_ranges = []
    for pairs in load_pairs_column_no:
        r = []
        for col_no in pairs:
            r.append(col_no+str(start_row_no)+":"+col_no+str(end_row_no))
        load_pair_ranges.append(r)
    return load_pair_ranges

def get_single_range(start_row_no, end_row_no, col_no):
    r_out = col_no+str(start_row_no)+":"+col_no+str(end_row_no)
    return r_out

load_pair_ranges = get_load_pair_ranges(start_row_no, end_row_no, load_pairs_column_no)
beam_size_range = get_single_range(start_row_no, end_row_no, beam_size_column_no)
beam_length_range = get_single_range(start_row_no, end_row_no, beam_length_column_no)
design_sheet = wb_design.sheets[design_sheet_name]
out_sheet = wb_out.sheets[summary_sheet_name]

beam_sizes = out_sheet.range(beam_size_range).value
beam_lengths = out_sheet.range(beam_length_range).value

load_pairs = []
for loads_by_case in load_pair_ranges:
    i, j = loads_by_case[0], loads_by_case[1]
    Mu = out_sheet.range(i).value
    Pu = out_sheet.range(j).value
    load_pairs.append((Mu,Pu))

n_beams = len(beam_sizes)
DCR = [0]*n_beams

# =============================================================================
# Plug and play between spreadsheet
# =============================================================================
for n in range(load_cases):
    Mu, Pu = load_pairs[n]
    dcr_col = DCR_output_cols[n]
    for i in range(n_beams):
        design_sheet[LenLoc].value = beam_lengths[i]
        design_sheet[PuLoc].value = Pu[i]
        design_sheet[MuLoc].value = Mu[i]
        design_sheet[MemLoc].value = beam_sizes[i]
        DCR[i] = round(design_sheet[DcrOut].value,2)
        out_sheet[dcr_col+str(i+start_row_no)].value = DCR[i]