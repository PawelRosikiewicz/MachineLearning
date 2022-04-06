# ********************************************************************************** #
#                                                                                    #
#   Project: Data Frame Explorer                                                     # #                                         # 
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


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os # allow changing, and navigating files and folders, 
import sys
import re # module to use regular expressions, 
import glob # lists names in folders that match Unix shell patterns
import random # functions that use and generate random numbers

import numpy as np # support for multi-dimensional arrays and matrices
import pandas as pd # library for data manipulation and analysis
import seaborn as sns # advance plots, for statistics, 
import matplotlib as mpl # to get basic plt   functions, heping with plot mnaking 
import matplotlib.pyplot as plt # for making plots, 

from sklearn.datasets import make_classification # creates simple data egxample
from sklearn.metrics import confusion_matrix
from itertools import product


# Function, ...................................................
def plot_confusion_matrix(X, y, model, with_perc=False, figsize=(4,3), cmap="Reds"):
    '''creates annotated heatmap for confusion matrix
        . X; 1D or 2D array, with input data
        . y; numpy vector with target variable
        . model; trained model, or pipeline
        . with_perc; displays nr and % of each class, 
    '''
    # crreate confuciton matrics
    matrix = confusion_matrix(y_true=y, y_pred=model.predict(X))
    
    # add row/col description, and place it in dataframe
    matrix = pd.DataFrame(
        matrix,
        columns=[f'pred:{x}' for x in range(matrix.shape[1])],
        index=[f'True:{x}' for x in range(matrix.shape[0])]
    )
    
    if with_perc==True: 
        # calulate percentate of each True class for heatmap annotation
        'to ensure that I get % of true class in each row, I will use loop, sorry'
        True_class_counts = matrix.sum(axis=1).to_list()
        matrix_perc = matrix.copy()
        for col in range(matrix.shape[1]):
            matrix_perc.iloc[:, col] = matrix.iloc[:, col]/True_class_counts[col]
            
        # create labels for heatmap cells
        labels = matrix.copy()
        for comb in product(range(matrix.shape[0]), repeat=2):
            value = matrix.iloc[comb[0],comb[1]]
            perc = np.round(matrix_perc.iloc[comb[0],comb[1]]*100,1)
            labels.iloc[comb[0],comb[1]] = f'{value}\n{perc}%'        
        
        # plot the results with annotated heatmap 
        plt.figure(figsize = figsize)
        sns.heatmap(matrix, annot=labels, fmt='', cmap=cmap)          
              
    elif with_perc==False:
        # plot the results with annotated heatmap 
        plt.figure(figsize = figsize)
        sns.heatmap(matrix/matrix.sum(), fmt=".2%",
                annot=True, cmap=cmap)

    plt.show();
    