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
    
    
    
    
# Fucntion, .............................
def plot_decision_surface(X, y, model, scatter_dct=dict()):
    ''' Plots decision surface for classyficaiton models with 2D data
        Caution, this function works only for 2D input data, because it has to create all combinaitons of value
        . X       - input data for building a model
        . y       - target variable,
        . model  - clasifier, wiht fucntion predict.proba()
        . scatter_dct - dct with additional arguments for scatterplot
    '''
       
    # find labels
    labels = pd.Series(y).unique().tolist()
    
    # plot scatter witch points in X,y
    for label in labels:
        label_idx = y==label
        plt.scatter(X[:, 0][label_idx], 
                    X[:, 1][label_idx],
                         label=label,
                        **scatter_dct
                      )
    
    # ..(b).. Create a grid of values (all combinations of values)
    lim          = [X.min(), X.max()]
    x_values     = np.linspace(*lim, num=40)
    y_values     = np.linspace(*lim, num=40)
    xx, yy       = np.meshgrid(x_values, y_values)  # meshgrid, returns two arrays 40x40
    points       = np.c_[xx.flatten(), yy.flatten()]

    """
        meshgrid:
        -------------------------------------------------
        for y retunrs an rrays as foolow    3 3 3 3 ... 3
                                            2 2 2 2 ... 2
        and for x, number are repeated      . . . .     .
        in each column,                     0 0 0 0 ... 0
    """
    
    # ..(c).. Calulate Probability for positive class (setosa) 
    #.        at every point on a mesh
    probs = model.predict_proba(points)[:, 1]

    
    # ..(d).. Draw decision boundary (p=0.5)
    zz = probs.reshape(xx.shape) # makes array 40x40
    plt.contour(xx, yy, zz, levels=[0.5], colors='gray') # line on top of probits, 
    
    # ..(e).. Plot decision surface with level curves
    plt.contourf(xx, yy, zz, 10, alpha=0.3, cmap=plt.cm.coolwarm) # red-blue colors below all points, 

    # ....... Add labels
    plt.xlabel('petal length (cm)')
    plt.ylabel('petal width (cm)')
    plt.legend()
    plt.colorbar(label='probability')
    plt.show();
   