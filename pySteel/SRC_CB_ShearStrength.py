# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:07:40 2019

@author: SMadhavan
"""
import aisc_shapes_database as ad
import os

## EMBEDMENT EFFECTS ON FLEXURAL STRENGTH
def compute_Leff_LeffRatio(L, Le):
    Leff = L+2*Le/3 #inches; effective length
    ratio = L/Leff
    return (Leff, ratio)

def compute_VatMp(Mp, L):
    # If Mp in kip-in and L in inches
    VatMp = 2*Mp/L #kips; 
    return VatMp
    
def compute_Mn_VatMn(Mp, VatMp, ratio):
    Mn = ratio*Mp #kip-in; Nominal moment strength
    VatMn = ratio*VatMp #kips; Shear corresponding to nominal moment strength
    return (round(Mn), round(VatMn))

## SHEAR STRENGTH COMPUTATION (UNITS IN KIPS AND INCHES)
def compute_Vp(Fy, d_steel, tw_steel):
    Aw = d_steel*tw_steel #in^2; Area of web of steel beam
    Vp = 0.6*Fy*Aw #kip; Nominal shear strength of steel section
    return Vp
    
def compute_Vne (Vp, f_ce_psi, bc, dc, A_st, fy_te, s, Ry_steel):
    #Expected Shear Strenth Calc
    Ve_steel = 1.1*Ry_steel*Vp #kip
    Ve_concrete = 1.42*(0.17*(f_ce_psi**0.5)*bc*dc)/1000 #kip
    Ve_stirrup = 1.33*(A_st*fy_te*dc)/s #kip
    Vne = round(Ve_steel + Ve_concrete + Ve_stirrup)
    return Vne
    
def compute_Vn(Vp, f_c_psi, bc, dc, A_st, fy_t, s):
    #Nominal Shear Strength Calc
    V_steel = Vp #kip
    V_concrete = 0.17*(f_c_psi**0.5)*bc*dc/1000 #kip
    V_stirrup = (A_st*fy_t*dc)/s #kip
    Vn = round(V_steel + V_concrete + V_stirrup)
    return Vn


## EMBEDMENT SHEAR STRENGTH - (H4-1) ANSI/AISC 341-16 Seismic Provisions
def compute_Vn_embed(f_c, t, b, beta_1, L, Le, c):
    """
    NOTE: f_c is in ksi here
    t = wall thickness the beam embeds into (inches)
    b = bearing width (equal to flange width for wide-flange steel sections) (inches)
    beta_1 = ACI stress block factor
    c = depth of spalling assumed equal to the depth of wall clear cover (inches)
    L = clear span length (inches)
    Le = length of embedment (inches)
    """
    temp1 = 1.54*(f_c**0.5)*((t/b)**0.66)*beta_1*b*(Le-c)
    temp2 = (0.58-0.22*beta_1)/(0.88+(L+2*c)/(2*(Le-c)))
    Vn_embed = temp1*temp2 #kips
    return round(Vn_embed)

def compute_Cb(Vne_limit, beta_1, L, Le, c):
    temp1 =(L+2*c)/(2*(Le-c))
    temp2 = (temp1+0.33*beta_1)/(0.88-0.33*beta_1)
    Cb = temp2*Vne_limit #kips
    return round(Cb)

if __name__ == "__main__":
    
    #Concrete material
    f_c = 8 #ksi; Specified compresive strength of concrete
    Ry_conc = 1.3 #ratio of expected to specified compressive strength of concrete
    beta_1 = 0.65 # (a/c) for 8ksi concrete
    
    #Concrete Section
    bc = 18 #inches; beam width (effective width of concrete encasement)
    d = 20 #inches; full depth of beam
    clear_cover = 1.5 #inches; 
    
    #Transverse reinforcement
    area_transverse_rebar = 0.31 #in^2; #5 bar
    n_legs_transverse = 2 #2 legs of stirrup
    fy_t = 80 #ksi; Specified yield strength 
    fy_te = 85 #ksi; expected yield strength of transverse reinforcement
    s = 4 #inches; spacing of transverse reinforcement
    
    #Structural Steel Material
    Fy = 50 #ksi; specified minimum yield strength of steel
    Ry_steel = 1.1 #ratio of expected to specified minimum yield strength of structural steel
    
    #Structural Steel Section
    section_name = "W14X120"
    filepath = os.getcwd()+r"\aisc-shapes-database-v15.0_local.xlsx"
    aisc_shapes_database, aisc_descriptors = ad.load_aisc_database(filepath)
    section_params = ad.get_section_from_name(aisc_shapes_database, section_name)
    #d_steel, inches; Depth of steel beam
    #tw, inches; Thickness of web of steel beam
    #bf, inches; Width of flange
    #tf, inches; Thickness of flange
    d_steel, tw, bf, tf = section_params[['d', 'tw', 'bf', 'tf']].values[0]

    
    #Element geometry
    L = 65 #inches; clear span of beam
    Le = 48 #inches; embedment of steel beam on either side inside the beam wall interface
    
    #Embedment properties
    t = 18 #inches; Thickness of wall, the beam embeds into
    cc_wall = 0.75 #inches; clear cover of wall
    
    #Capacity
    Mpe = 1.1*24550 #kip-in; plastic flexural strength calculated from plastic stress or strain compatibility analysis with specified material properties
    
    #Calculated Parameters
    f_ce = Ry_conc*f_c #ksi; Expected compressive strength of concrete
    f_c_psi = f_c*1000 #f_c in psi
    f_ce_psi = f_ce*1000 #f_ce in psi
    dc = d - clear_cover #inches; effective depth of concrete encasement
    A_st = n_legs_transverse*area_transverse_rebar #in^2 per unit spacing; area of transverse reinforcement
    
    #Computing V@Mne
    Leff, ratio = compute_Leff_LeffRatio(L, Le)
    VatMpe = compute_VatMp(Mpe, L)
    Mn, VatMne = compute_Mn_VatMn(Mpe, VatMpe, ratio)
    print("VatMne = ",VatMne, " kips")
    
    #Computing Vne
    Vp = compute_Vp(Fy, d_steel, tw)
    Vne = compute_Vne(Vp, f_ce_psi, bc, dc, A_st, fy_te, s, Ry_steel)
    print("Vne = ",Vne," kips")
    
    #Computing Vne_limit
    Vne_limit = min(Vne, VatMne)
    print("Vne_limit = ",Vne_limit," kips")
    
    #Computing Vn_embed
    Vn_embed = compute_Vn_embed(f_ce, t, bf, beta_1, L, Le, cc_wall)
    print("Vne_embed = ",Vn_embed, " kips")
    
    #Computing Cb
    Cb = compute_Cb(Vne_limit, beta_1, L, Le, cc_wall)
    print("Cb = ",Cb, " kips")

    
