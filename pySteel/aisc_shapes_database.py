# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:39:04 2019
@author: SMadhavan
"""

import pandas as pd

def load_aisc_database(filepath):
    xls = pd.ExcelFile(filepath)
    aisc_shapes_database = pd.read_excel(xls, sheet_name = "Database v15.0")
    aisc_descriptors = pd.read_excel(xls, sheet_name = "v15.0 Readme Condensed")
    return aisc_shapes_database, aisc_descriptors

def get_section_from_name(aisc_shapes_database, section_name):
    section = aisc_shapes_database[aisc_shapes_database["EDI_Std_Nomenclature"] == section_name]
    return section

def get_sections_by_filter(aisc_shapes_database, filter_label, filter_on):
    sections = aisc_shapes_database[aisc_shapes_database[filter_on].str.contains(filter_label)]
    return sections

def get_filtered_sections_by_name(aisc_shapes_database, filter_label, filter_on = "EDI_Std_Nomenclature"):
    sections = get_sections_by_filter(aisc_shapes_database, filter_label, filter_on)
    return sections    

def get_WF_params(section, aisc_descriptors):
    select_params = ['d','bf','tw','tf','Ix', 'Zx', 'Iy', 'Zy', 'ry']
    WF_param = section[select_params]#.to_dict(orient = 'records')
    WF_descriptors = aisc_descriptors[aisc_descriptors['Variable'].isin(select_params)][['Variable','Description']]
    return WF_param, WF_descriptors