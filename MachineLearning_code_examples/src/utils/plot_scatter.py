# ********************************************************************************** #
#                                                                                    #
#   Project: Data Frame Explorer                                                     #                         
#   Author: Pawel Rosikiewicz                                                        #
#   Contact: prosikiewicz(a)gmail.com                                                #
#                                                                                    #
#   License: MIT License                                                             #
#   Copyright (C) 2021.01.30 Pawel Rosikiewicz                                       #
#                                                                                    #
# Permission is hereby granted, free of charge, to any person obtaining a copy       #
# of this software and associated documentation files (the "Software"), to deal      #
# in the Software without restriction, including without limitation the rights       #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell          #
# copies of the Software, and to permit persons to whom the Software is              #
# furnished to do so, subject to the following conditions:                           #
#                                                                                    # 
# The above copyright notice and this permission notice shall be included in all     #
# copies or substantial portions of the Software.                                    #
#                                                                                    #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR         #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,           #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE        #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER             #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,      #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE      #
# SOFTWARE.                                                                          #
#                                                                                    #
# ********************************************************************************** #



# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import random
import glob
import re
import os
import seaborn as sns

from matplotlib import colors
import matplotlib.patches as patches



# Function, ......................................................
def test_outlier_removal_with_zscore(
    data_df,
    names,
    zscore_cutoff=2, 
    add_noise=True,
    include_zeros=True,
    title="",
    figsize=(12, 14),
    nrows=5, 
    ncols=4
    ):
    """ creates scatterplots with each feature in df in separate subplot.
        x-axis: log1p tranformed data, y.axis: raw data
        the funciton can add random noise to points on both x,y axes (add_noise=True), 
        to allow visualizations of mutiple points with the same values, 
        eg: many points can have the same value, eg. 0, and these poeints become visible
        on the ploot after adding small noise

        + I ADDED MEAN VALIUE AND POTENTIAL Z-.SCORE THAT COULD 
          BE USED AT CUTOFF TO FILTER OUT OUTLIERS, 

        + NUMBER OF DATA POINTS WITH NON-MISSING DATA AND POINTS THAT WOUDL 
          BE REMOVED IN CASE THAT FILTER WOUDFL BE USED, WERE CALULATED 
          AND DIPLAYED IN TITLE OF EACH SUBPLOT,
          
        parametrs: 
        - data_df; pandas dataframe
        - names; list, len()==data_df.shape[1]
        - zscore_cutoff; 
        - add_noise; bool, if True, random noise is added to points, to allow their visualizations, 
            ie. many points can have the same value, eg. 0, and these poeints become visible
            on the ploot after adding small noise
        - include_zeros; whther to use zero values on the plot, 
        - title; str, for figure title
    """

    # work on copy, 
    data_df = data_df.copy()
    continuous_features = names

    # set style, and fig parameters,  
    plt.style.use("default")
    scatter_point_style = {"s":14, "c":"green", "alpha":.5, "edgecolor":"white"}
    
    # figure
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, facecolor="white")
    fig.suptitle(title, fontsize=20)

    # Subplots,
    for i, ax in enumerate(axs.flat):
        if i+1 > len(continuous_features): 
            break

        # Prepare y values, by addint a bit of noise for scatter plot 
        #.        - so i can see how many points is everywhere
        y_val = data_df[continuous_features[i]].dropna().values
        noise = np.random.normal(loc=0, scale=np.std(y_val)/4, size=y_val.shape)
        
        y_val_log = np.log1p(data_df[continuous_features[i]].dropna().values)
        small_noise = np.random.normal(loc=0, scale=np.std(y_val_log)/20, size=y_val_log.shape)
        
        # Scatter plot
        if add_noise==True:
            ax.scatter(x= y_val_log+small_noise, y=y_val+noise, **scatter_point_style)
        else:
            ax.scatter(x= y_val_log, y= y_val, **scatter_point_style)
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))
        ax.yaxis.set_major_locator(plt.MaxNLocator(3))
        ax.set(xlabel="log1p values", ylabel=f"raw data")
        sns.despine()

        # Add lines showing mean and ±threshold (in sd units) to plot,
        if include_zeros==True:
            ax.axvline(y_val_log.mean(), color="red", linestyle="--", linewidth=3, label="mean")
            ax.axvline(y_val_log.mean()-y_val_log.std()*zscore_cutoff, color="orange", linestyle="--", linewidth=2, label="z-cutoff")
            ax.axvline(y_val_log.mean()+y_val_log.std()*zscore_cutoff, color="orange", linestyle="--", linewidth=2)
            ax.legend(loc='upper left', frameon=True)

            # Calculate number of included points, 
            total_nr          = len(y_val_log)
            excluded_point_nr = np.logical_or(y_val_log<y_val_log.mean()-y_val_log.std()*zscore_cutoff, 
                                              y_val_log>y_val_log.mean()+y_val_log.std()*zscore_cutoff).sum() 
            # Subplot title wiht info:
            ax.set_title(f"{continuous_features[i]}\ndata points ={total_nr}, exluded={excluded_point_nr}" )
            
    # Aestetics, 
    plt.tight_layout() # to avoid overlapping with the labels
    plt.subplots_adjust(top=0.82)
    plt.show();
    
    
    
    

  

  
  