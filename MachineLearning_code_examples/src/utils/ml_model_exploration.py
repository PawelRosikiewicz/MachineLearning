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




# Function, ...................................................
def make_classification_and_fit_model(model, mc_dct=None, plot=False, verbose=False):
    ''' creates enviroment to fit, and test the classyficaiton model
        returns fitted model, and the data/labels for train and test data
        . model; sklearn model or pipeline
        . mc_dct; dictionary with parameters for makie_classificaiton function
        . plot; bool, if True, it creates a scatterélot with descision boundary, 
                    on the first 2 features as xy axes.
        . verbose; bool, if True, funciton prins model test acc, data/label shape, 
          and scatterplot with the first two features, and makers separating samples 
          from different classes with the color, 
        
        Caution ! i didnt synchronized class and background colors, if you use >3 classes, 
        these colos may not fit to each other.
          
    '''
    # default settings for make_classyficaiton
    if pd.isnull(mc_dct):
        mc_dct={"n_samples":1000, "n_features":2, "n_classes":2, "random_state":0,
                "n_informative":2, "n_redundant":0, "n_repeated":0, "n_clusters_per_class":1
        }
    else:
        pass

    # create the data
    X, y = make_classification(**mc_dct)    

    # split into train/test sets
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.3, random_state=0)

    # fit the model
    model.fit(X_tr, y_tr);

    # plot decision boudaries on the first two features
    if plot==True:
        # find labels
        labels = pd.Series(y).unique().tolist()

        # plot scatter witch points in X,y
        plt.rcParams["figure.figsize"] =[4,3]
        for label in labels:
            label_idx = y==label
            plt.scatter(X[:, 0][label_idx], 
                        X[:, 1][label_idx],
                        label=label,
                        s=2,
            )

        # create a grid of values (all combinations of values)
        lim = [X.min(), X.max()]
        list_of_values = [np.linspace(*lim, num=100)]*X.shape[1]
        mesh = np.meshgrid(*list_of_values)
        for i, values in enumerate(mesh):
            if i==0:
                data_points = values.flatten()
            else:   
                data_points = np.c_[data_points, values.flatten()]

        # Compute predictions for mesh data_points
        mesh_preds = model.predict(data_points)

        # rehape predicitons so they correspond with the plot and feature dimensions
        mesh_preds = mesh_preds.reshape(mesh[0].shape)
        if mesh_preds.ndim>2:
            mesh_preds = mesh_preds[:,:,0]
        else:
            pass

        # plot decision surface with level curves
        plt.contourf(
            list_of_values[0], list_of_values[0], 
            mesh_preds, alpha=0.3, 
            cmap=plt.cm.coolwarm) # red-blue colors below all points,     

        # Add labels
        plt.legend()
        plt.show();
    
    else:
        pass

    # report results
    if verbose==True:
        print("data: ", X.shape)
        print("labels: ", y.shape)     
        print(f'Accuracy: {model.score(X_te, y_te)}')
    else:
        pass

    # return trained model and the data
    return model, X_tr, X_te, y_tr, y_te    
  
  
  
  
  
  
  