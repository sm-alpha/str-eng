# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:47:39 2020

@author: SMadhavan
"""
import numpy as np
import profile_generators_v2 as pg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rc('font', family='DejaVu Sans', size = 16)
plt.rc('xtick', labelsize='medium')
plt.rc('ytick', labelsize='medium')
COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']

def plot_collector_diagram(gridline, story, df_filtered, fig_folderpath = '', save_fig = False, close_fig = False):
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    x_tot = df_filtered['Location']
    fig, ax = plt.subplots(3,1, figsize = (16,12), sharex=True, sharey=True)
    fig.text(0.5, 0.02, 'Length (ft)', ha='center', fontsize = 20, style = 'italic')
    fig.text(0.5, 0.97, 'Collector '+gridline+', '+story, ha='center', fontsize = 20, fontweight = 'bold')
    fig.text(0.02, 0.5, 'Force (kip)', va='center', rotation='vertical', fontsize = 20, style = 'italic')
    plt.tight_layout(pad = 4, h_pad = 0)
    plt.subplots_adjust(hspace = 0.2, top = 0.9)
    for i in range(2, 5):
        p = i-2
        R = df_filtered.iloc[:,i]
        xi, yi = pg.get_shear_profile(x_tot, R)
        ax[p].plot(xi, yi, marker = 'o', markersize = 6, color = colors[p])
        if p<2:
            ax[p].tick_params(axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False)
        ax[p].set_title(df_filtered.columns[i], pad = 15)
        ax[p].grid(True, alpha = 0.3)
        ax[p].axhline(y = 0, color = 'k', alpha = 0.2)
        ax[p].set_xlim(left = x_tot[0], right = x_tot[-1])
        ax[p].spines['top'].set_visible(False)
        ax[p].spines['right'].set_visible(False)
        ax[p].spines['bottom'].set_visible(False)
        ax[p].spines['left'].set_visible(False)
        for xz, yz in zip(xi, yi):
            label = "{:.0f}".format(yz+0)
            ax[p].annotate(label, (xz, yz), textcoords="offset points", xytext=(15,-15), ha = 'center', fontsize = 16)
    if save_fig:
        plt.savefig((fig_folderpath + "/{0}, {1}.png").format(gridline, story), dpi = 300)
    if close_fig:
        plt.close()
    return None

def plot_shear_diagram(story, df_filtered, fig_folderpath = '', 
                       colors = COLORS, save_fig = False, close_fig = False):
    x_tot = df_filtered['Location']
    fig, ax = plt.subplots(3,1, figsize = (16,12), sharex=True, sharey=True)
    fig.text(0.5, 0.02, 'Length (ft)', ha='center', fontsize = 20, style = 'italic')
    fig.text(0.5, 0.97, 'Diaphragm shear '+story, ha='center', fontsize = 20, fontweight = 'bold')
    fig.text(0.02, 0.5, 'Force (kip)', va='center', rotation='vertical', fontsize = 20, style = 'italic')
    plt.tight_layout(pad = 4, h_pad = 0)
    plt.subplots_adjust(hspace = 0.2, top = 0.9)
    for i in range(3, 6):
        p = i-3
        R = df_filtered.iloc[:,i]
        xi, yi = pg.get_shear_profile(x_tot, R)
        ax[p].plot(xi, yi, marker = 'o', markersize = 6, color = colors[p])
        if p<2:
            ax[p].tick_params(axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False)
        ax[p].set_title(df_filtered.columns[i], pad = 15)
        ax[p].grid(True, alpha = 0.3)
        ax[p].axhline(y = 0, color = 'k', alpha = 0.2)
        ax[p].set_xlim(left = x_tot[0], right = x_tot[-1])
        ax[p].spines['top'].set_visible(False)
        ax[p].spines['right'].set_visible(False)
        ax[p].spines['bottom'].set_visible(False)
        ax[p].spines['left'].set_visible(False)
        for xz, yz in zip(xi, yi):
            label = "{:.0f}".format(yz+0)
            ax[p].annotate(label, (xz, yz), textcoords="offset points", xytext=(15,-15), ha = 'center', fontsize = 16)
    if save_fig:
        plt.savefig((fig_folderpath + "/Shear {0}.png").format(story), dpi = 300)
    if close_fig:
        plt.close()
    return None

def plot_moment_diagram(story, df_filtered, fig_folderpath = '', 
                       colors = COLORS, save_fig = False, close_fig = False):
    x_tot = df_filtered['Location']
    fig, ax = plt.subplots(3,1, figsize = (16,12), sharex=True, sharey=True)
    fig.text(0.5, 0.02, 'Length (ft)', ha='center', fontsize = 20, style = 'italic')
    fig.text(0.5, 0.97, 'Diaphragm moment: '+story, ha='center', fontsize = 20, fontweight = 'bold')
    fig.text(0.02, 0.5, 'Corrected Moment (kip-ft)', va='center', rotation='vertical', fontsize = 20, style = 'italic')
    plt.tight_layout(pad = 4, h_pad = 0)
    plt.subplots_adjust(hspace = 0.2, top = 0.9)
    for i in range(3, 6):
        p = i-3
        R = df_filtered.iloc[:,i]
        xi, *temp, yi = pg.get_moment_profile(x_tot, R)
        ax[p].plot(xi, yi, color = colors[p])
        if p<2:
            ax[p].tick_params(axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False)
        ax[p].set_title(df_filtered.columns[i], pad = 15)
        ax[p].grid(True, alpha = 0.3)
        ax[p].axhline(y = 0, color = 'k', alpha = 0.2)
        ax[p].set_xlim(left = x_tot[0], right = x_tot[-1])
        ax[p].spines['top'].set_visible(False)
        ax[p].spines['right'].set_visible(False)
        ax[p].spines['bottom'].set_visible(False)
        ax[p].spines['left'].set_visible(False)
        max_id = np.argmax(yi)
        min_id = np.argmin(yi)
        x_ann = [xi[max_id], xi[min_id]]
        y_ann = [yi[max_id], yi[min_id]]
        for xz, yz in zip(x_ann, y_ann):
            label = "{:.0f}".format(yz+0)
            ax[p].annotate(label, (xz, yz), textcoords="offset points", xytext=(15,-15), ha = 'center', fontsize = 16)
    if save_fig:
        plt.savefig((fig_folderpath + "/Moment {0}.png").format(story), dpi = 300)
    if close_fig:
        plt.close()
    return None