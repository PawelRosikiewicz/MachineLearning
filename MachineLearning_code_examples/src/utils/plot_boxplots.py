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



# Function, ............................................................
def ordered_boxplots(df, yvar, axvars, title=""):
    '''
        creates boxlots, of one numeric variable (yvar), clustered with >=1 ordinal/indicator variables,
        + caulates correlation between median in each cluster, and the. response/target variable, 
        and. orders. automatically, subplots, starting from the variable combinaiton wiht the highest corr. coef.
        
        - df       pandas dataframe, with target variable (numeric), and indicator variables (numeric, text, object, or int)
        - yvar     str, colname, with responsse variable name in df
        - axvars   list[str,...], colanmes of indicator. variables in df, 
        - title    str, figure title,
    '''

    # data
    df = pd.DataFrame(df).copy()
    df.reset_index(drop=True, inplace=True)    
 
    # find medians of each class, and order the classes acordingly, 
    corr_res = []
    for i, axvar in enumerate(axvars):    
        # find orer of boxes, 
        grp       = df.groupby(by=axvar)
  
        # turn classes, into integers == means
        key_values_df = grp.median().loc[:,yvar]
        classes = key_values_df.index.values.tolist()
        medians = key_values_df.values.tolist()
            
        # replace class values with class medians
        num_axvar = pd.Series([0]*df.shape[0])
        for c, m in zip(classes,  medians):
            idx = df.loc[:,axvars[i]]==c  
            num_axvar.iloc[idx]=m
        num_axvar.reset_index(drop=True, inplace=True)
    
        # correlation 
        corr_value = pd.concat([num_axvar,df.loc[:,yvar]], axis=1).corr().iloc[0,1]
            
        # append results
        corr_res.append({
            "axvar": axvar,
            "corr_value": corr_value
        })

    # create dataframe & find subplot order, 
    corr_res  = pd.DataFrame(corr_res)
    corr_res  = corr_res.sort_values("corr_value", ascending=False)
    corr_res.reset_index(inplace=True, drop=True)
    # ..
    ordered_axvars = corr_res.axvar.values.tolist()
    
    # Figure,
    fig, axs = plt.subplots(
        nrows=int(np.ceil(len(ordered_axvars)/4)), 
        ncols=4, 
        figsize=(15,15), 
        facecolor="white"
    )
    fig.suptitle(title, fontsize=20)
    
    # .. subplots,
    for i, ax in enumerate(axs.flat):
        if i>=len(ordered_axvars):
            # ensure empty subplot, for no. more data in the row
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines['top'].set_visible(False) # remove ...
            ax.spines['right'].set_visible(False) # remove ... 
            ax.tick_params(axis='x', colors='white') # tick only
            ax.tick_params(axis='y', colors='white') # tick only    
            ax.yaxis.set_ticks_position('left')# shows only that
            ax.xaxis.set_ticks_position('bottom')# shows only that
            #break
        else:          
            # find orer of boxes, 
            grp       = df.groupby(by=ordered_axvars[i])
            box_order = grp.median().loc[:,yvar].sort_values().index

            # correlation 
            corr_value = corr_res.corr_value.loc[corr_res.axvar==ordered_axvars[i]].values
            
            # boxplot
            sns.boxplot(y=yvar, x=ordered_axvars[i], data=df, ax=ax, order=box_order)
            ax.set_title(f"{ordered_axvars[i]}\ncorr={np.round(corr_value,3)}")

            # axes labels
            ax.set_xlabel("")
            ax.set_ylabel(f'{yvar}')

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

    # .. Aestetics, 
    plt.tight_layout()
    plt.subplots_adjust(top=.9)
    plt.show();