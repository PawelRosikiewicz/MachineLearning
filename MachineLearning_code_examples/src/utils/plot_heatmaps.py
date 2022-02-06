
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





# find, potential correlations
def corr_heatmap(*,df,figsize=(10,10), 
                           cmap="RdBu", 
                           method='pearson', 
                           title="Correlation Matrix",
                           min_max_values=(-1,1)
                          ):
    '''
        ................................................................
        Creates heatmap with correlation matrix, 
                using one of the three selected methods, 
        ................................................................
        cmap.  : matplotlib cmap, eg: {"RdBu", "Plasma", "coolwarm"}
        title  : str, if empty,  = Correlation Matrix + method
        df     : pandas dataframe
        method : {'pearson', 'kendall', 'spearman'} from df.corr()
                * pearson : standard correlation coefficient
                * kendall : Kendall Tau correlation coefficient
                * spearman : Spearman rank correlation    
        min_max_values: vmin, and vmax from matplotlib.axes.Axes.imshow     
           
        Comments:
        you may also use seaborn function that will give alsmot the same results,        
        >>> corr = data_df.corr()
        >>> sns.heatmap(corr, 
                xticklabels=data_df.select_dtypes(['number']).columns,
                yticklabels=data_df.select_dtypes(['number']).columns)
        >>> plt.show();        
    '''
    # calculate correlations
    df_corr = df.copy().corr()
        
    # set style, and fig parameters,  
    plt.style.use("default")
    labelsize=8
    ticks_style ={"fontsize":labelsize}
    
    # figure    
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    fig.suptitle(f'{title} - {method}', fontsize=20) 
    im = ax.matshow(df_corr, cmap=cmap, vmin=min_max_values[0], vmax=min_max_values[1])
                   
    # ticks
    ax.set_xticks(range(df.select_dtypes(['number']).shape[1])) 
    ax.set_xticklabels(df.select_dtypes(['number']).columns, rotation=45, ha="left", **ticks_style)
    ax.set_yticks(range(df.select_dtypes(['number']).shape[1]))
    ax.set_yticklabels(df.select_dtypes(['number']).columns, ha="right", **ticks_style)

    # remove axes, & ticks you dont want to see
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("top")

    #colorbar
    cb = fig.colorbar(im, extend="both", shrink=0.5)
    cb.ax.tick_params(labelsize=labelsize)
    plt.show();
    
    
    
# Function, ........................................................
def table_with_sorted_corr_results(df, method='pearson'):
    '''
        ................................................................
        returns dataframe, with 3 columns (names of compared features, and correlation coeff.)
        results are sorted with absolute values, so that, the pair of variables wiht the highest corr. 
        coeff, +&- will be on the top 
        ................................................................
        df: dataframe, pandas, 
        method : {'pearson', 'kendall', 'spearman'} or callable
    '''
    # corr
    corr_res = df.corr(method=method)
    abs_corr_res = corr_res.abs()

    # combinations
    rows, cols = np.indices((corr_res.shape[0], corr_res.shape[1]))
    idx_mesh = pd.Series([(i,j) if i!=j else None for i, j in zip(rows.ravel(),cols.ravel())])
    idx_mesh = idx_mesh.loc[idx_mesh.notnull()]
    
    # extract feature names
    results = []
    for idxx in idx_mesh:
        # get feature names and sort to later on find duplicates, 
        feature_names = [
            corr_res.index.values.tolist()[idxx[0]],
            corr_res.columns.values.tolist()[idxx[1]]
        ]
        feature_names.sort()

        # add values to dict and create dataframe
        results.append({
            "first":feature_names[0],
            "second":feature_names[1],
            "corr":corr_res.iloc[idxx[0], idxx[1]],
            "corr_abs": np.abs(corr_res.iloc[idxx[0], idxx[1]])
        })

    # prepare sorted dataframe without duplicates
    df_res = pd.DataFrame(results)
    df_res = df_res.drop_duplicates(["first", "second"],keep="first")
    df_res = df_res.sort_values("corr_abs", ascending=False).iloc[:,0:3]
    df_res.reset_index(drop=True, inplace=True)

    return df_res
  
  

  
