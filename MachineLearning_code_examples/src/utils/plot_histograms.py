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

from scipy import stats
from matplotlib import colors
import matplotlib.patches as patches





# Function, ......................................................
def plot_histograms(*, df, names, title=""):
    '''
        produce nice looking histograms for data in each column in input dataframe
        each histogram has unique color, thus it is easy to compare these histograms on different plots, 
        with different data transfomration methods
        - df;  dataframe or numpy array,
        - feature_names; list, len==df.shape[1]
        - title; str, use for fig.suptitle()
    '''

    df = pd.DataFrame(df)
    
    # prepare colorset, - can be used as cmap, 
    cmap = mpl.cm.get_cmap('tab10')
    rgba = cmap(np.linspace(0,1,len(names)))
    
    # Figure, 
    fig, axs = plt.subplots(
        nrows=1, 
        ncols=len(names), 
        figsize=(len(names)*2, 2), 
        facecolor="white"
    )

    # Subplots,
    for i, ax in enumerate(axs.flat):
        if i+1 > len(names): 
            break
    
        # hist
        fig.suptitle(title, fontsize=14)
        ax.hist(
            df.iloc[:,i], 
            bins=30, 
            color=rgba[i], 
            histtype="stepfilled", 
            edgecolor="black"
        )
        ax.set_title(names[i])
        ax.xaxis.set_major_locator(plt.MaxNLocator(2))
        ax.yaxis.set_major_locator(plt.MaxNLocator(3))
        sns.despine()

    # Aestetics, 
    plt.tight_layout() # to avoid overlapping with the labels
    plt.subplots_adjust(top=0.7)
    plt.show();
  
  
  

  
  
# Function, ..............................................................................
def feature_distribution(df, col):
    """
        plots
        1. histogram
        2. boxplot
        3. probanblity plot
        for one numerical variable in df
        - df; pandas dataframe
        - col; column name

        taken from: https://www.kaggle.com/mustafacicek/simple-eda-functions-for-data-analysis
    """
    
    skewness = np.round(df[col].skew(), 3)
    kurtosis = np.round(df[col].kurtosis(), 3)

    fig, axes = plt.subplots(1, 3, figsize = (21, 7))
    
    sns.kdeplot(data = df, x = col, fill = True, ax = axes[0], color = "#603F83", linewidth = 2)
    sns.boxplot(data = df, y = col, ax = axes[1], color = "#603F83",
                linewidth = 2, flierprops = dict(marker = "x", markersize = 3.5))
    stats.probplot(df[col], plot = axes[2])

    axes[0].set_title("Distribution \nSkewness: " + str(skewness) + "\nKurtosis: " + str(kurtosis))
    axes[1].set_title("Boxplot")
    axes[2].set_title("Probability Plot")
    fig.suptitle("For Feature:  " + col)
    
    for ax in axes:
        ax.set_facecolor("#C7D3D4FF")
        ax.grid(linewidth = 0.1)
    
    axes[2].get_lines()[0].set_markerfacecolor('#8157AE')
    axes[2].get_lines()[0].set_markeredgecolor('#603F83')
    axes[2].get_lines()[0].set_markeredgewidth(0.1)
    axes[2].get_lines()[1].set_color('#F1480F')
    axes[2].get_lines()[1].set_linewidth(3)
    
    sns.despine(top = True, right = True, left = True, bottom = True)
    plt.show()  
  
  
  
  
  
  
  

# Function, ........................................................
def multiple_sns_displots(
    df, names, figsize=None, 
    figscale=1, nrows=1, 
    color=None, cmap='tab10', 
    title="", distplot_dct={}):
  
    ''' ................................................................
        Returns nice looking histograms with sns.distplot function, 
        organized as subplots, 
        ................................................................
        parameters
        - df;  dataframe or numpy array,
        - feature_names; list, len==df.shape[1]
        - figscale; float, def==1, affect figure size, and fonsizes, 
        - nrows; int, def==1, how many rows to use, for subplots,  
        - color; str, or None, if str value provided, all histograms will have that color, 
        - cmap, str, matplotlib cmap, 
        - title; str, use for fig.suptitle()
        - distplot_dct; dictionary, with parameters for sns.displot()
        returns
        - matplotlib figure, 
    '''

    # work on copy of df subset
    assert isinstance(df, pd.core.frame.DataFrame), "df must be dataframe"
    df = pd.DataFrame(df.loc[:,names].copy()).copy()
    
    # rows/cols number
    nrows=nrows 
    ncols=int(np.ceil(len(names)/nrows))  
    
    # figsize
    if pd.isnull(figsize):
        figsize=(len(names)*3*figscale/nrows, 2*figscale*nrows)
    else:
        pass
    
    # prepare colorset, - can be used as cmap, 
    #.   cmap = mpl.cm.get_cmap('tab10')
    #.   rgba = cmap(np.linspace(0,1,len(names)))
    if pd.isnull(color):
        colors = sns.color_palette(cmap, len(names))
    else:
        colors = [color]*len(names)
    
    # Figure, 
    fig =plt.figure( figsize=figsize, facecolor="white")
    fig.suptitle(title, fontsize=10*figscale)
    
    # add each subplot separately,
    '''done this way, because other axs.flat doent work well with sns objects'''
    ax_number = 0 
    for irow in range(nrows):
        for icol in range(ncols):
            ax_number +=1
            
            if ax_number > len(names): 
                # no plot, but keep empty space
                break
                
            else:
                # add
                ax = fig.add_subplot(int(nrows), int(ncols), int(ax_number))
                ax = sns.distplot(            
                    df.iloc[:,ax_number-1], 
                    color=colors[ax_number-1],
                    **distplot_dct
                )
                
                # labels
                ax.set_title(names[ax_number-1], fontsize=14*figscale)
                ax.set_xlabel("", fontsize=4*figscale)
                ax.set_ylabel("", fontsize=4*figscale)
                
                
                ax.xaxis.set_major_locator(plt.MaxNLocator(2))
                ax.yaxis.set_major_locator(plt.MaxNLocator(3))

                # remove axes, & ticks you dont want to see
                ax.yaxis.set_ticks_position("left")
                ax.xaxis.set_ticks_position("bottom")                
                
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

    # Aestetics, 
    plt.tight_layout() # to avoid overlapping with the labels
    
    if title=="":
        pass
    else:
        plt.subplots_adjust(top=0.8)
    plt.show();