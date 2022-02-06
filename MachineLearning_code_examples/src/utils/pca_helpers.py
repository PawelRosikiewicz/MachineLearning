# ********************************************************************************** #
#                                                                                    #
#   Project: Data Frame Explorer                                                     #                         
#   Author: Pawel Rosikiewicz                                                        #
#   Contact: prosikiewicz(a)gmail.com                                                #
#                                                                                    #
#   License: MIT License                                                             #
#   Copyright (C) 2021.11.25 Pawel Rosikiewicz                                       #
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




# Function, ........................................................
def plot_pca_resutls(
    pca_results, 
    indicators_df, 
    indicators, 
    components=(0,1), 
    cmap='Paired', 
    cmap_range=(0,0.5), 
    figsize=(5,4), 
    title_fontsize=20,
    scatter_dct = {},
    legend_dct = {}
):

    """
        plots figures wiht data projected on the first two components, 
        points classified with selected categorical features have different colors, 

        parameters
        -------------------------------------------------------------
        - pca_results,    numpy arr, with resutls from pca.transform()
        - indicators_df,  dataframe, with indicator variables, 
                           must indicators_df.shape[1]==pca_results.shape[1]
        - indicators;     list, with column names in indicators_df
        - components      tuple, default, (0,1), list of components to plot, 
                           also dimension, in pca_results[:, <components>]  
        - cmap            matplotlib cmap name
        - cmap_range      tuple, with two floats [0,1], value range from, to in cmap, to sample colors
        kwargs:
        - scatter_dct     from plt.scatter
        - legend_dct      from plt.legend  
                          
    """
    data_df = pd.DataFrame(indicators_df)

    # plot figures wiht data projected on the first two components
    for stratifier in indicators:
        components = (0,1)

        # searched value
        s = data_df.loc[:,stratifier]

        # replace na with "unknownw"
        s.fillna("unknown", inplace=True)

        # get all unique classes in a stratifier, 
        '''start from the most frequent, so the samll classes are visible on the plot'''
        s_unique_values = s.value_counts().sort_values(ascending=False).index.values.tolist()

        # prepare colorset, - can be used as cmap, 
        cmap = mpl.cm.get_cmap(cmap)
        rgba = cmap(np.linspace(cmap_range[0],cmap_range[1],len(s_unique_values)))

        # fig & title
        fig, ax = plt.subplots(ncols=1, nrows=1, facecolor="white", figsize=figsize)
        fig.suptitle(stratifier, fontsize=title_fontsize)

        # make plot for each dataploint
        for i,k in enumerate(s_unique_values):
            idx = np.where(s==k)[0].tolist()
            ax.scatter( 
                pca_results[idx, components[0]],                
                pca_results[idx, components[1]],         
                color=rgba[i],
                label=f'{k}',
                **scatter_dct
            )

        # legend
        lg = ax.legend(frameon=True, scatterpoints=1, **legend_dct)
        frame = lg.get_frame()
        frame.set_alpha(0.2)
        frame.set_facecolor("grey")
        frame.set_edgecolor("darkgrey")
        
        # axes labels
        ax.set_xlabel(f'principial component {components[0]}')
        ax.set_ylabel(f'principial component {components[1]}')
 
        # Remove ticks, and axes that you dot'n want, format the other ones,
        ax.spines["left"].set_visible(True)
        ax.spines["bottom"].set_visible(True)
        # ...
        ax.spines['top'].set_visible(False) # remove ...
        ax.spines['right'].set_visible(False) # remove ... 

        # Format ticks,
        ax.tick_params(axis='x', colors='black', direction='out', length=4, width=2) # tick only
        ax.tick_params(axis='y', colors='black', direction='out', length=4, width=2) # tick only    
        ax.yaxis.set_ticks_position('left')# shows only that
        ax.xaxis.set_ticks_position('bottom')# shows only that

        plt.show();
        





