# ********************************************************************************** #
#                                                                                    #
#   Project: Data Frame Explorer                                                     #                         
#   Author: Pawel Rosikiewicz                                                        #
#   Contact: prosikiewicz(a)gmail.com                                                #
#                                                                                    #
#   License: MIT License                                                             #
#   Copyright (C) 2022.03.20 Pawel Rosikiewicz                                       #
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



# Function, .................................................................
def scatter2D(X, y, features=(0,1), cmap="hsv", figsize=(4,3)):
    ''' plots first two features in numpy array, with scatterplot
        labels are shown as differernt colors
        . X - np.array, numeric dtype, 
        . y - vetor with labels,  
        . features = tuple, selected feaures to plot, integers, 
        . figsize - tuple, two int, for figure size
    '''
    # set style: default
    plt.style.use("default")
    
    # select colors for plot
    marker_colors = plt.get_cmap(cmap)(np.linspace(0, 0.8, len(np.unique(y).tolist())))
    
    # scatterplot
    'created in loop, to have label handles for legend'
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize, facecolor="white")
    for i, class_name in enumerate(np.unique(y).tolist()):
        ax.scatter(X[y==class_name,features[0]], 
                   X[y==class_name,features[1]], 
                   s=5, alpha=0.8, 
                   color=marker_colors[i],
                   label=str(class_name)
                  )
    ax.set(xlabel=f"featue No{features[0]}", ylabel=f"feature No{features[1]}")
    sns.despine()
    
    # add legend
    lg = plt.legend(scatterpoints=1, frameon=True, 
              labelspacing=1, title="legend")
    frame = lg.get_frame()
    frame.set_color("lightgrey")
    frame.set_edgecolor("grey")
    
    # finally, 
    plt.show();