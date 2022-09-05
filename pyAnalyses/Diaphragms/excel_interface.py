# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 21:11:23 2020

@author: SMadhavan
"""
import pandas as pd
import xlwings as xw

def get_excel_range(start_row_no, end_row_no, start_col_no, end_col_no):
    r_out = start_col_no+str(start_row_no)+":"+end_col_no+str(end_row_no)
    return r_out

def get_df_from_input(excel_filepath, sheet_name, data_range, empty = 0.0):
    wb = xw.Book(excel_filepath)
    xl_sheet = wb.sheets[sheet_name]
    df = xl_sheet.range(data_range).options(pd.DataFrame, index = False, empty = empty).value
    return df

def get_xl_sheet_from_input(excel_filepath, sheet_name):
    wb = xw.Book(excel_filepath)
    xl_sheet = wb.sheets[sheet_name]
    return xl_sheet