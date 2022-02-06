# ************************************************************************* #
#                                                                           #
#                                                                           #
#                                                                           #  
#              - - -    EPFL-ext Module 3  HELPER    - - -                  #     
#                        BY PAWEL ROSIKIEWICZ                               #
#                                                                           #
#                                                                           #
#                       last update: 2020.04.01                             #
#                                                                           #
#     Author:   Pawel Rosikiewicz                                           #       
#     Copyrith: IT IS NOT ALLOWED TO COPY OR TO DISTRIBUTE                  #
#               these file without written                                  #
#               persmission of the Author                                   #
#     Contact:  prosikiewicz@gmail.com                                      #
#                                                                           #
#                                                                           #
# ************************************************************************* #



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
import scipy.stats as stats

import pandas.api.types as ptypes

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, HuberRegressor, SGDRegressor
from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV # builtin cross-validation, test many alphas, return best one, 

from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_squared_error as MSE




#### Class, .............................................................................

class PandasPreprocessorHousePrices():
    """
        .............................................................
        Custom made transformer for House Price Data
        .............................................................

        IMPORTANT 
        - this function can transforms only dataframes, with named columns, 
        - it can not work with pandas series,
        - it can not have namne duplicates in rows and columns in df,

        FUNCTIONS
        . fit_transfomr()        : see below fit transfomed policy
        . fit()                  : see below, 
        . get_df_summary(self)   : returns summary of df before and after fit transform (pd.DataFrame)
        . get_params(self)       : it will return all parameters, including df summary
        . get_list_of_binary_transofmed_variables(self) : for dev. purposes

        .............................................................
        FIT TRANSFORM POLICY,
        .............................................................

        . MISSING DATA: 
            - function removes all missing data in df, 
                -  if na% >= THRESHOLD (required by __init__), then the variable is replaced by the binary indicator var. present/absent
                otherwise:
                - if the var is nominal/has less then, 10 unique numbers(classes), na us replaced with most frequent value
                - if the var is numeric with >10 classes, it uses median
            
        . ORDINAL VARIABLES, 
            - column names specified in __init__
            - na replaced with string, "no value",
        
        . CONTINUOUS VARIABLES, 
            - specified in __init__
            - log tranformed (np.log1p)
            - added polynomial features, as specified in __init__ defautl = [0.5, 2, 3, 5] 
                 
        . ALL TEXT VARIABLES:
            - one-hot-encoding perfomed with pd.get_dummy(), after prevoius tranformations 
            - columns created for the first value is removed, (alphabetical or numerical order)


        .............................................................
        FIT NEW DATASET, 
        .............................................................
        . MISSING DATA, 
            - such as most frequent and mendian, saved for fit() function for new datasets
            - all columns have replacement policy build, even if they dont have any missing data
            - one-hot-encoding - if variables is missing, collumn with zeros will be added, 
        . UNKNOWN VARIABLES;
            - ignored, 
            - unknownw columns are removed, 
    """

    # ------------------------------------------------------------------------------
    # PRIVATE METHODS AND VARIABLES,     

    # Function, .....................................................................
    def __init__(self, NaTr_for_binary_transfomration=0.9):
        
        self._na_tr                       = NaTr_for_binary_transfomration # used to decide on columns tranformed into indicator binary variables
        self._fit_params_dct              = dict()
        self._columns_to_remove_tuple     = ["Order", "PID", "SalePrice"] # or None
        #self._transform_ordinal_variables = transform_ordinal_variables
        self._polynomials                 = [0.5, 2, 3, 4, 5] # or None
        
        self._ordinal_variables           = [
            "Exter Qual", "Exter Cond", "Bsmt Qual", "Bsmt Exposure", "Heating QC",
            "Electrical", "Kitchen Qual", "Functional", "Garage Finish", "Garage Qual"
            "Garage Cond", "Paved Drive"
            ] # values may, or may not be replaced with ascenting numbers       
        
        self._dummy_ordinal_variables     = [
            "Lot Shape", "Utilities", "Land Slope", "BsmtFin Type 1", 
            "BsmtFin Type 2","Fireplace Qu", "Fence"
            ] # these must still have NA values replaced
    
    
        self._continuous_features = [
            'Lot Frontage', 'Lot Area', 'Mas Vnr Area', 'BsmtFin SF 1', 'BsmtFin SF 2',
            'Bsmt Unf SF', 'Total Bsmt SF', '1st Flr SF', '2nd Flr SF', 'Low Qual Fin SF',
            'Gr Liv Area', 'Garage Area', 'Wood Deck SF', 'Open Porch SF', 'Enclosed Porch',
            '3Ssn Porch', 'Screen Porch', 'Pool Area', 'Misc Val'
            ] # i will apply log1p tranformation to these variables, 

              
    # Function, .....................................................................     
       
    def __inspect_df_dtypes(self, df):

        # to start with, 
        assert type(df)==pd.DataFrame
        col_dtype_table = list() 

        # collect the info, on each column,
        for i, col in enumerate(list(df.columns)):
            col_dtype_table.append(
                {
               "col_name":col,
               "is_string_dtype": ptypes.is_string_dtype(df.loc[:,col]),
                "is_numeric_dtype": ptypes.is_numeric_dtype(df.loc[:,col]),
                "col_dtype": df.loc[:,col].dtypes,
                "na_nr": df.loc[:,col].isnull().sum(),
                "row_nr": df.shape[0] 
                })
                                
        # return pd.DataFrame   
        return pd.DataFrame(col_dtype_table) 
    

    # Function, .....................................................................

    def __remove_selected_columns(self, df, colName_list=None):
        """
            fucntion to remove columns, if they exist,
            in case the list will be empty, or not given function will not work, 
        """
        if colName_list==None:
            "do nothing"
    
        else:
            # Test input df
            assert type(df) == pd.DataFrame, "Incorrect obj type"
            df = df.copy() # to work on a cop
            
            # test input df dimensions, 
            if df.shape[1]<2:
                return df # return whatever, there is, because removing any column, woould remove all the data, in df
            
            else:
                # remove, if possible, 
                for i, colName in enumerate(colName_list):
                    "i - unused, in this version"
                    try:
                        # test input df dimensions, at each iteration, 
                        if df.shape[1]<2:
                            "no action"
                        else:
                            df.drop(columns=[colName], axis=1, inplace=True)
                    except:
                        "do nothing"

            # Return,
            return df        
        
    
    # Function, ..................................................................... 
      
    def __replace_values_in_variables_with_too_many_nan(self, 
        df, 
        tr=0.9,  # ie col must have at least 90% of nan to be considered
        col_list=[],       
        fit=True                                           
    ):
        """
            Function, check whther the columns have too many rows with missing data,
            if yes, all no-na values, are replaces with "Some_value", and all na with "No_value"
            
            col_threshold   : float, default is, 0.5, min. percentage of rows with missing data
                              in a given columns, that is required to perfom procedure, 
                              
            tr : fit_tranfomed will use self.NaTr_for_binary_transfomration                  
                              
        """
        
        # to start, 
        assert type(df)== pd.DataFrame, "Incorrect obj type" # Test input df,
        df = df.copy()   # work on a copy
        
        
        if fit==True:
            
            col_list = list()
        
            # check each column, and decide, 
            for i, col in enumerate(list(df.columns)):
                row_filter = df.loc[:,col].isnull().values # np.arr
                reverse_filter = row_filter==False # np.arr

                # check if you have more (>=) na then specified by th ethreshold, 
                if tr <= row_filter.sum()/df.shape[0]:
                    
                    # create new indicator variable
                    df.loc[:,col] = df.loc[:,col].astype(object)
                    df.loc[row_filter,col] = "No_value"
                    df.loc[reverse_filter,col] = "Some_value"
                    
                    # save columns name to the list for transomf funcion
                    col_list.append(col)

                else:
                    "no action"
                    
            # return
            return df, col_list
        
        # else use col_list to create indicator variables, 
        else:
            
            if len(col_list)==0:
                "there is nothing to transform"
                
            else:
                # check each column, and decide, 
                for i, col in enumerate(col_list):

                    try:
                        row_filter = df.loc[:,col].isnull().values # np.arr
                        reverse_filter = row_filter==False # np.arr

                        df.loc[:,col] = df.loc[:,col].astype(object)
                        df.loc[row_filter,col] = "No_value"
                        df.loc[reverse_filter,col] = "Some_value"

                    except:
                        "no action, probably no column was detected"
                    
            # return
            return df
            
                 
    # Function, .....................................................................

    def __replace_nan_with_one_specified_value(self, df, column_names, new_value):
        """
            replacing nan values, with one provided value,  
        """
        
        # Test input df,
        assert type(df) == pd.DataFrame, "Incorrect obj type"
        df = df.copy()  # to work on a copy,

        # replace na values in each column, 
        for i, col_name in enumerate(column_names):
            
            # try, beacuse not all rows, may be available, 
            try:
                row_filter = df.loc[:,col_name].isnull()
                df.loc[row_filter,col_name] = new_value
            except:
                "do nothing"

        # return:
        return df           
        

    # Function, ..................................................................... 

    def __find_replacement_values_for_nan_in_each_column(self, 
        df,
        df_col_names=None, 
        min_class_nr=10, 
        fill_na=0
    ):
        """
            .................   .................................................................... 
            Property            Description
            .................   ....................................................................             

            Function            replacing nan with most frequent class member(text and numeric types)
                                or with median (numeric types)          
                                Supporty only {numeric, text} pandas dtypes,                
            parameters
            ...................                    
            * df                pd.DataFrame
            * df_col_names      list, with column names to be ussed for nan, replacing
                                introduced, here, to be able to select subset of columns, and
                                use thast fucntion in case some columns have unknownw NaN
                                if None, all columns will be used,
            * min_class_nr      int, Most frequent member of a class, is used, 
                                when the numeric types have <= number of classes 
                                then min_class_nr, default =10
            * fill_na           {int, str, float}, value that should be placed instead of nan
                                in columns that have only nan.
                                
            returns
            ...................
            pd.DataFrame        copy with the above modiffications, 
            logger_dct          dictionary, {"columnName":<value used to replace NaN>}
        
        """
        # to start, 
        assert type(df)== pd.DataFrame, "Incorrect obj type"
        assert type(min_class_nr)== int
        df = df.copy()   # work on a copy
        
        # dct with the results, 
        replacement_values_dct = dict()
        
        # column names
        if df_col_names==None:
            df_col_names = list(df.columns)
        
        
        # work on each column separately,         
        for i, col in enumerate(df_col_names): 

            # in case there are only missing data
            if df[col].isnull().sum()==df.shape[0]:
                replacement_values_dct[col]  = fill_na
                
            else: 
                # in case there is only one value
                if df.loc[:,col].unique().size==1:
                    replacement_values_dct[col]  = df[col].unique()[0]
                    
                else:
                    # use most frequent value, to replace NA in text features, 
                    if ptypes.is_string_dtype(df.loc[:,col]):        
                        replacement_values_dct[col]   = df.loc[:,col].dropna().value_counts().sort_values(ascending=False).index[0]
                  
                    # numeric types
                    if ptypes.is_numeric_dtype(df.loc[:,col]):

                        # use most frequent, if there is less then 11, classes
                        if (df.loc[:,col].unique().shape[0]>0) and (df.loc[:,col].unique().shape[0]<=min_class_nr): 
                            replacement_values_dct[col]   = df.loc[:,col].dropna().value_counts().sort_values(ascending=False).index[0]
                            
                        # use median to replace NA in numeric features, with >10 different values
                        if df.loc[:,col].unique().shape[0]>min_class_nr:
                            replacement_values_dct[col]  = np.median(df[col].dropna().values) 
        # return,
        return replacement_values_dct
            
        

        
        
    # Function, .....................................................................

    def __replace_nan_with_pre_selected_values(self, df, new_values_dct):
        """
            replacing nan values, where it is possible, using the 
            dictionary created with self.__find_replacement_values_for_nan_in_each_column()
        """
        
        # Test input df,
        assert type(df) == pd.DataFrame, "Incorrect obj type"
        df = df.copy()  # to work on a copy,

        # replace na values in each column, 
        for key, value in new_values_dct.items():

            # try, beacuse not all rows, may be available, 
            try:
                na_postion              = df.loc[:,key].isnull()
                df.loc[na_postion,key]  = value
            except:
                "do nothing"

        # return:
        return df


    # Function, .................................................................

    def __one_hot_encoder(self, df):

        """
            fit_transform() & transfomr()
            Finds variables to perfomr one hot encoding, transforms them,
        """

        # to start with, 
        assert type(df)==pd.DataFrame
        df = df.copy()     

        # find columns to transform,
        df_summary          = self.__inspect_df_dtypes(df = df)
        cn_filter           = df_summary.is_string_dtype==True
        cols_for_oneHotEnc  = df_summary.col_name.loc[cn_filter].values.tolist()

        """
                    example of the results

                        col_dtype           col_name  is_numeric_dtype  is_string_dtype  na_nr  \
                    0   float64        MS SubClass              True            False      0   
                    1     uint8  MS Zoning_A (agr)              True            False      0   # DUMMY 0/1 ARE uint8 dtype !
                    2     uint8  MS Zoning_C (all)              True            False      0   
                    3     uint8       MS Zoning_FV              True            False      0   
                    4     uint8  MS Zoning_I (all)              True            False      0  
        """

        # iterate over these columns, and add new encoded features, 
        if len(cols_for_oneHotEnc)>0:
            for c_ith, col_name in enumerate(cols_for_oneHotEnc):

                # add new columns with dummy variables, 
                df = pd.concat([
                    df,
                    pd.get_dummies(
                        df.loc[:, col_name], 
                        prefix=f'dummy {col_name}', # to avoid having colnamne duplicates
                        drop_first = True, # drop one of the dummies as required by certain statistical methods
                        dummy_na=True  # create dummy variables for NaN's
                        )
                    ],axis=1)


                # now remove original column, from df
                df = df.drop(col_name, axis=1)

        # return
        return df    

 
    # ------------------------------------------------------------------------------

    # CLASS METHODS
    
  
    # Function, .....................................................................  
      
    def get_df_summary(self):
        "returns summary of df before and after fit transform (pd.DataFrame)"
    
        return [self._fit_params_dct[f'df_summary_before_fit_transform'], 
                self._fit_params_dct[f'df_summary_after_fit_tranform']]
    

    # Function, .....................................................................

    def get_params(self):
        """i wrote it because I was not satisfied with results returned by BaseEstimator, 
          it will return all parameters, including df summary"""
        
        for key, value in self._fit_params_dct.items():
            print(f"{''.join(['.']*60)}")
            print(key)
            print(f"{''.join(['.']*60)}")
            print(value, end="\n\n")
            
        
    # Function, .....................................................................

    def get_list_of_binary_transofmed_variables(self):
        "I had to test that object because i had problmes with that particuls part, "
    
        mlist = self._fit_params_dct["new_binary_indicator_variables"]
        return mlist    
    
      
    # Function, .....................................................................

    def fit_transform(self, df, verbose=False):
        """
            . function removes all missing data in df, 
              - if na% >= tr, then the variable is replaced by the binary indicator var. present/absent
              otherwise:
                - if the var is nominal/has less then, 10 unique numbers(classes), na us replaced with most frequent value
                - if the var is numeric with >10 classes, it uses median
            
           . ordinal variables, specified in __init__
               - na replaced with string, "no value",
        
           . continuous variables, specified in __init__
               - log tranformed (np.log1p)
               - added polynomial features, as specified in __init__
                 defautl = [0.5, 2, 3] 
                 
            . all text variables:
                - one-hot-encoding perfomed with pd.get_dummy()
                
            . missing data, such as most frequent and mendian, saved for fit() function
              for test datasets
        """
        
        # Test input df,
        assert type(df) == pd.DataFrame, "Incorrect obj type"
        df = df.copy() # to work on a copy

        
        # (0) check, dtyes in all columns,
        #.    -------------------------------------
        self._fit_params_dct[f'fit_transform timestamp']         = str(pd.to_datetime("now"))
        self._fit_params_dct[f'df_summary_before_fit_transform'] = self.__inspect_df_dtypes(df = df)
                      
        
        # (1) Pre-set modiffications, 
        #.    -------------------------------------
        
        # ... Drop pre-selected columns, if they are present, 
        modified_df = self.__remove_selected_columns(
            df=df, 
            colName_list=self._columns_to_remove_tuple)
                  
            
        # ... Replace NA in ordinal variables,
        modified_df = self.__replace_nan_with_one_specified_value(
            df = modified_df, 
            column_names=self._ordinal_variables, 
            new_value="Not_available"
        )
        
        modified_df = self.__replace_nan_with_one_specified_value(
            df = modified_df, 
            column_names=self._dummy_ordinal_variables, 
            new_value="Not_available"
        )        

        
        # ... introduce indicator variable, in place of variables with too many NaN, 
        #.    ie. in these cases, I assumed, that I hasve too many missing data, to relicably, 
        #.        replace them with median/most frequent variable, 
        modified_df, col_name_list = self.__replace_values_in_variables_with_too_many_nan( 
            df=modified_df, 
            tr=self._na_tr,
            fit=True
        )
        self._fit_params_dct["new_binary_indicator_variables"]=col_name_list
    
   

        # (2) Data Imputation,
        #.    -------------------------------------
        
        # ... Find values to replace nan in all other columns, 
        self._fit_params_dct["nan replacement values"] = self.__find_replacement_values_for_nan_in_each_column(
            df=modified_df, 
            df_col_names=None, 
            min_class_nr=10, # if numberic varibale has 10 or less, unique values, it will be treated as nominal variable, 
            fill_na=0
        )
    
        # ... and replace nan with values that were found in step before, 
        modified_df = self.__replace_nan_with_pre_selected_values(  
            df=modified_df, 
            new_values_dct=self._fit_params_dct['nan replacement values']
        )
    
    
        # (3) [optional] change some pre-select text ordinal variables into dicrete ordinal variables, 
        #.    -------------------------------------
            # if self._transform_ordinal_variables == True:
              
               
                
        # (4) One-hot encoding,  
        #.    -------------------------------------    
        """
            (only text features, numeric variables are omitted) 
            simple appraoch, that didn't work, very well: ie was generating errors from time to time,
            modified_df = pd.get_dummies(modified_df, dummy_na=True) # ie. do not create new columns for NA,
                                                                  # DUMMY 0/1 ARE uint8 dtype !        
        """
        modified_df = self.__one_hot_encoder(df=modified_df)   
            
                
        # (5) Log-tranform + polynomial features, 
        #.    -------------------------------------
        for i, c in enumerate(self._continuous_features):
            try:
                if (modified_df.columns.values==c).sum()==1:
                    
                    # log tranform,
                    modified_df[c] = np.log1p(modified_df[c].values)
                
                    # add polynomial values
                    if self._polynomials!=None:
                        for d in self._polynomials:
                            new_col_name = f'{c}**{d}'
                            modified_df[new_col_name] = modified_df[c].values**d
                    else:
                        "do not add polynomial features"
                else:
                    "do nothig, column not found"
            except:
                "no action"
        
                
        # (6) check, dtyes in all columns,
        #.    -------------------------------------
        
        df_summary = self.__inspect_df_dtypes(df = modified_df)
        self._fit_params_dct['df_summary_after_fit_tranform'] = df_summary 
        
        if verbose==True:
            all_numeric = (df_summary.is_numeric_dtype==True).sum()==df_summary.shape[0]
            no_missing_data= (df_summary.na_nr==0).sum()==df_summary.shape[0]

            if no_missing_data!=True:
                " - Warning - "
                "Fit tranform is incomplete - at least one variable has MISSING DATA, use get_df_summary() to find it"
            if all_numeric!=True:
                " - Warning - "
                "Fit tranform is incomplete - at least one variable IS NOT NUMERIC TYPE, use get_df_summary() to find it"

        # Final Step, return  
        #.    -------------------------------------
        return modified_df    

           
    # Function, .....................................................................

    def transform(self, df, store_df_summary=False, verbose=False):
        """
            . function removes all missing data in df, 
              using information saved in dct, after fit_tranform.
            
           . ordinal variables, specified in __init__
               - na replaced with string, "no value",
        
           . continuous variables, specified in __init__
               - log tranformed (np.log1p)
               - added polynomial features, as specified in __init__
                 defautl = [0.5, 2, 3] 
                 
            . all text variables:
                - one-hot-encoding perfomed with pd.get_dummy()
        """     
        
        # Test input df,
        assert type(df) == pd.DataFrame, "Incorrect obj type"
        df = df.copy() # to work on a copy
        df_timestamp = str(pd.to_datetime("now"))
  
        if verbose==True:
            store_df_summary=True


        # (0) check, dtyes in all columns,
        #.    -------------------------------------
        if store_df_summary==True:
            self._fit_params_dct[f'df_summary_before_transform {df_timestamp}'] = self.__inspect_df_dtypes(df=df)
                      
    
        # (1) Pre-set modiffications, 
        #.    -------------------------------------
        
        # ... Drop pre-selected columns, if they are present, 
        modified_df = self.__remove_selected_columns(
            df=df, 
            colName_list=self._columns_to_remove_tuple)
                  
            
        # ... Replace NA in ordinal variables,
        modified_df = self.__replace_nan_with_one_specified_value(
            df = modified_df, 
            column_names=self._ordinal_variables, 
            new_value="Not_available"
        )
        
        modified_df = self.__replace_nan_with_one_specified_value(
            df = modified_df, 
            column_names=self._dummy_ordinal_variables, 
            new_value="Not_available"
        )        

        # ... tranform pre-select variables into binary indicator variables
        list_with_colnames = self._fit_params_dct["new_binary_indicator_variables"]
        modified_df = self.__replace_values_in_variables_with_too_many_nan( 
            df=modified_df, 
            col_list=list_with_colnames,
            fit=False
        )

          
        # (2) Data Imputation, 
        #.    -------------------------------------  
        
    
        # ... Replace nan with values that were found in step before, 
        modified_df = self.__replace_nan_with_pre_selected_values(  
            df=modified_df, 
            new_values_dct=self._fit_params_dct['nan replacement values']
        )
    
        # (3) [optional] change some pre-select text ordinal variables into dicrete ordinal variables, 
            # if self._transform_ordinal_variables == True: NOT USED AT ALL, ....
              
                # NOT IMPLEMENTED - IT WAS TAKING TO MUCH TIME, TO RUN THAT FUNCTION WITHOUT IMPROVING THE MODELS MUCH, 
                
                
        # (4) One-hot encoding,  
        #.    -------------------------------------
        """
            (only text features, numeric variables are omitted) 
            simple appraoch, that didn't work, very well: ie was generating errors from time to time,
            modified_df = pd.get_dummies(modified_df, dummy_na=True) # ie. do not create new columns for NA,
                                                                  # DUMMY 0/1 ARE uint8 dtype !        
        """
        modified_df = self.__one_hot_encoder(df=modified_df) 
            
                     
        # (5) Log-tranform + polynomial features, 
        #.    -------------------------------------
        
        for i, c in enumerate(self._continuous_features):
            try:
                if (modified_df.columns.values==c).sum()==1:
                    
                    # log tranform,
                    modified_df[c] = np.log1p(modified_df[c].values)
                
                    # add polynomial values
                    if self._polynomials!=None:
                        for d in self._polynomials:
                            new_col_name = f'{c}**{d}'
                            modified_df[new_col_name] = modified_df[c].values**d
                    else:
                        "do not add polynomial features"
                else:
                    "do nothig, column not found"
            except:
                "no action"
  

        # (6) add missing columns and remove columns with unknown vartiables, 
        #.    -------------------------------------
        """
            eg: dummy viariables, will be created only using unique values in a columns 
                in new df, thus, in some cases there will be missing or additional values that may
                not been present in training dataset used for fit_transform.
                From that reason I remove all uknonwn variables, and replace all missing variables, with zeros, (ie. absent)
                ....
                columns shoudl be in the same order,
        """            

        # get column names and order from fit_transform(), 
        df_summary = self._fit_params_dct['df_summary_after_fit_tranform']
        col_list_in_order = df_summary.col_name.to_list()
        """
            df_summary;
                        col_dtype           col_name  is_numeric_dtype  is_string_dtype  na_nr  \
                    0   float64        MS SubClass              True            False      0   
                    1     uint8  MS Zoning_A (agr)              True            False      0
        """          
        
        # reindex, new df, 
        modified_df = modified_df.reindex(columns=col_list_in_order, fill_value=0) 
                      # this shodul remove all unknonw, or add any missing variable, 
            
        # (7) check, dtyes in all columns,
        #.    -------------------------------------
        
        if store_df_summary==True:
            df_summary  = self.__inspect_df_dtypes(df = modified_df)
            self._fit_params_dct[f'df_summary_after_transform {df_timestamp}'] = df_summary
            
            if verbose==True:
                all_numeric = (df_summary.is_numeric_dtype==True).sum()==df_summary.shape[0]
                no_missing_data= (df_summary.na_nr==0).sum()==df_summary.shape[0]

                if no_missing_data!=True:
                    " - Warning - "
                    "Fit tranform is incomplete - at least one variable has MISSING DATA, use get_df_summary() to find it"
                if all_numeric!=True:
                    " - Warning - "
                    "Fit tranform is incomplete - at least one variable IS NOT NUMERIC TYPE, use get_df_summary() to find it"
          
        # Final Step, return  
        #.    -------------------------------------
        return modified_df   









# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------

#   - - - FUNCTIONS USED IN MY PROJECT - - - 

# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------






# Function, .............................................................

def evaluate_features_in_df_using_simple_models(
    X_model, 
    y_model,
    test_size=0.2,
    verbose=True,
    number_of_random_states=4,
    model_complexity=1,
    ):
    """
        ..........................................................................................
        the function use input data with any number of features > model_complexity, 
        to run the same analyis as it woudl be done with more complex models, 
        using only 1-2 columns, run with several basic models, on several combinations 
        of radomly selected samples (rows) in X,y
        ..........................................................................................
        
        number_of_random_states   : int, >=1, number of time, the entire analysis 
                                    is rerapeated with different combination of rows in 
                                    train and in test data sets,
                                    
        model_complexity          : int, how many columns is being used to build models, 
                                    subsequelty used to evaklueat each featurew effect on MAE/MSE
                                    Currently, supported only 1 or 2, 
    """




    #### silo for the results,
    results = [] 


    #### Function Helper, 
    def real_MAE(y_te, predicted_y):
        """ calculates MAE for y values that werter transfomed on log scale, """

        # use np.e**<value>-1 to get real predicted and tater values, 
        real_y_te        = np.abs(((np.e**y_te)-1).astype("int"))
        real_predicted_y = np.abs(((np.e**predicted_y)-1).astype("int"))

        # calulate mae,
        mae = MAE(real_y_te,  real_predicted_y)

        # return,
        return mae


    #### Function Helper, 
    def real_MSE(y_te, predicted_y):
        """ calculates MSE for y values that werter transfomed on log scale, """

        # use np.e**<value>-1 to get real predicted and tater values, 
        real_y_te        = np.abs(((np.e**y_te)-1).astype("int"))
        real_predicted_y = np.abs(((np.e**predicted_y)-1).astype("int"))

        # calulate mae,
        mse = MSE(real_y_te,  real_predicted_y)

        # return,
        return mse



    #### Train all models, and baseline, calulate mae/mse and collect the results, 
    for random_state in range(number_of_random_states):


        # data preparation,

        # ... divide df's,
        X_tr, X_te, y_tr, y_te = train_test_split(
            X_model, 
            y_model, 
            test_size=test_size, 
            random_state=random_state)

        # ... min, max y values for clipping, predicitons,
        min_y = y_tr.min()
        max_y = y_tr.max()

        # ... Info,
        if verbose==True:
            print("--------------------------------------------")
            print(f"random state: {random_state}")
            print("--------------------------------------------")




        # Baseline,
        """ Baseline is calculated only once, for each random state """

        baseline_strategy = ["mean", "median"]
        id_numbers        = list(range(len(baseline_strategy)))
        for bs, id_for_groupby in zip(baseline_strategy, id_numbers):

            # ... fit baseline model, on  full data,  
            base = DummyRegressor(strategy=bs)
            base.fit(X_tr, y_tr)

            # Predict y values, using the baseline, and collect the results,
            results.append({
                            'method'            : f"baseline {bs}",
                            'meodel_complexity' : model_complexity,
                            'feature nr'        : len(list(X_tr.columns)),
                            'feature names'     : f"baseline {bs}",    # because it doents matter,
                            'random_state'      : random_state,
                             "ID"               : id_for_groupby,

                            # ......
                            'train_mae'      : MAE(y_tr,        base.predict(X_tr)),
                            'test_mae'       : MAE(y_te,        base.predict(X_te)),
                            'real_train_mae' : real_MAE(y_tr,   base.predict(X_tr)),
                            'real_test_mae'  : real_MAE(y_te,   base.predict(X_te)),

                            # ......
                            'train_mse'      : MSE(y_tr,        base.predict(X_tr)),
                            'test_mse'       : MSE(y_te,        base.predict(X_te)),
                            'real_train_mse' : real_MSE(y_tr,   base.predict(X_tr)),
                            'real_test_mse'  : real_MSE(y_te,   base.predict(X_te)),

                            # ....
                            'best_alpha': np.nan,
                            "best_l1": np.nan,

                            # .... and because t was easier to do that, 
                            'feature 1': f"baseline {bs}",
                            'feature 2': f"baseline {bs}",
                            'df_shape' : X_tr.shape
                })

        # for later on,
        id_for_groupby = len(baseline_strategy)

        # decide on model complexity, 
        columns_to_use   = list(X_tr.columns) 
        
        
        if model_complexity==1:
            combination_list = list()
            for i in range(len(columns_to_use)):
                combination_list.append([i])

        if model_complexity==2:
            
            import itertools
            
            items = list(range(len(columns_to_use)))
            combination_list = list()
            for subset in itertools.combinations(items, 2):
                combination_list.append(list(subset))

        if model_complexity>2:
            if verbose == True:
                print("ERROR the function supports only max complexity of level 2")
                # it is possible, but the number of combintaitons is too large, 

        # info, 
        if verbose == True:

            # progres bar, 
            N_stops_to_display_on_progres_bar = 4

            # some info on the begeinning, 
            print(f"Training model on {len(combination_list)} feature combinations\n...........................................")
            if N_stops_to_display_on_progres_bar<len(combination_list):
                N_stops_to_display_on_progres_bar==len(combination_list)
            reporting_pos = np.linspace(0,len(combination_list),N_stops_to_display_on_progres_bar).astype(int).tolist()
            one_nr = 0


        # loop, over each feature (complexity==1) or feature combination (complexity==2)
        for i, idx_comb in enumerate(combination_list):

            # info:
            if verbose==True:
                if i==reporting_pos[one_nr]:
                    print(f"Processing: {i+1} of {len(combination_list)}, with these columns as example: {idx_comb}")
                    one_nr+=1
                if i==len(combination_list)-1:
                    print("DONE\n...........................................")



            # (1) prepare df_subset with selected feature/s, for both train and test data

            # ... subset columns, 
            if model_complexity==1:
                X_tr_subset = X_tr.iloc[:,idx_comb]
                X_te_subset = X_te.iloc[:,idx_comb]
                feature_1 = list(X_tr_subset.columns)[0]
                feature_2 = ""

            if model_complexity==2:
                X_tr_subset = X_tr.iloc[:,[idx_comb[0], idx_comb[1]]]
                X_te_subset = X_te.iloc[:,[idx_comb[0], idx_comb[1]]]
                feature_1 = list(X_tr_subset.columns)[0]
                feature_2 = list(X_tr_subset.columns)[1]

                
            # (2) transfomr data,                

            # ... tranform data subsets,
            my_transformer     = PandasPreprocessorHousePrices(0.9) 
            X_tr_subset_transf = my_transformer.fit_transform(X_tr_subset)
            X_te_subset_transf = my_transformer.transform(X_te_subset)

            # ... Standardize features for some models,
            scaler                      = StandardScaler()
            X_tr_subset_transf_rescaled = scaler.fit_transform(X_tr_subset_transf) # calculate meas, SD's
            X_te_subset_transf_rescaled = scaler.transform(X_te_subset_transf)     # standarize



            
            # (3) instanciate selected models, and decide on hypeparameters for grid search, 

            # ...
            lr     = LinearRegression()
            huber  = HuberRegressor(epsilon=1.2)

            # ... 
            lr_sgd = SGDRegressor(
                loss='squared_loss',           #  Cost function
                penalty='none',                # Add a penalty term?, no not in this case, 
                max_iter=2000,                 # Number of iterations
                random_state=random_state,     # The implementation shuffles the data, the we will have always the same reult. 
                tol=1e-3                       # Tolerance for improvement (stop SGD once loss is below)
            )

            # .....
            alphas  = np.logspace(-1, 4, num=20)  
            ridgeCV = RidgeCV(alphas=alphas)   # Ridge with built in cross-validation 
            lassoCV = LassoCV(alphas=alphas, max_iter=10000, cv=3) # cv, determines, cv procedure, 3-fold, 

            # .....
            l1_ratios = np.linspace(0.01, 1, num=10)
            elasticCV   = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratios, cv=3)


            

            # (4) fit each model and collect the results,  

            for model, model_name in zip(
                    [lr, huber, lr_sgd, ridgeCV, lassoCV, elasticCV], 
                    ["lr", "huber", "lr_sgd", "ridgeCV", "lassoCV", "elasticCV"]
                ):
                
                # ... COUNTER - id number that will allo to gropupby methods without any problems
                id_for_groupby +=1
                
                # .... fit
                model.fit(X_tr_subset_transf_rescaled, y_tr)

                # .... Predict y values, using the model,
                predicted_y_tr = model.predict(X_tr_subset_transf_rescaled).clip(min=min_y, max=max_y)
                predicted_y_te = model.predict(X_te_subset_transf_rescaled).clip(min=min_y, max=max_y)

                # .... find best_alpha if applicable,
                if model_name=="ridgeCV" or model_name=="lassoCV" or model_name=="elasticCV":
                    best_alpha = model.alpha_
                else:
                    best_alpha      = np.nan

                # .... find best_l1 if applicable,
                if model_name=="elasticCV":
                    best_l1 = model.l1_ratio_
                else:
                    best_l1      = np.nan 

                # .... collect results,
                results.append({
                        'method'            : model_name,
                        'meodel_complexity' : model_complexity,
                        'feature nr'        : len(list(X_tr_subset.columns)),
                        'feature names'     : ", ".join(list(X_tr_subset.columns)),
                        'random_state'      : random_state,
                        "ID"                : id_for_groupby,

                        # ......
                        'train_mae'     : MAE(y_tr,   predicted_y_tr),
                        'test_mae'      : MAE(y_te,   predicted_y_te),
                        'real_train_mae': real_MAE(y_tr,   predicted_y_tr),
                        'real_test_mae' : real_MAE(y_te,   predicted_y_te),

                        # ......
                        'train_mse'     : MSE(y_tr,   predicted_y_tr),
                        'test_mse'      : MSE(y_te,   predicted_y_te),
                        'real_train_mse': real_MSE(y_tr,   predicted_y_tr),
                        'real_test_mse' : real_MSE(y_te,   predicted_y_te),

                        # ....
                        'best_alpha': best_alpha,
                        "best_l1": best_l1,

                        # .... and because t was easier to do that, 
                        'feature 1': feature_1,
                        'feature 2': feature_2,
                        'df_shape' : X_tr_subset_transf_rescaled.shape
            })  
                
    #### return,
    return results










# Function, .............................................................

def order_feature_and_plot_them(
    simple_models_df,
    feature_number = 1,
    value_to_use = "real_test_mae",
    sort_by = "median",
    y_limit = [20000, 60000],
    plot_title = "MAE caulated in simple models for each feature",
    verbose=True
):
    """
        ..........................................................................................
        orders the features in df, returned by evaluate_features_in_df_using_simple_models()
        according to selected metrics, returns, the list of ordered features, 
        and plot thast allows rto evaluate the resuls visually,
        ..........................................................................................
        
        * simple_models_df      : df, returned by evaluate_features_in_df_using_simple_models()                       
        * feature_number        : int, {1,2}, it is the same as model_complexity 
                                    set in evaluate_features_in_df_using_simple_models()                         
        * value_to_use          : str, {'real_test_mae', 'real_test_mse', 'real_train_mae',
                                           'real_train_mse', 'test_mae', 'test_mse', 
                                           'train_mae', 'train_mse'}                                    
        * sort_by               : str {'mean', 'median'}
        * y_limit               : list(int, int)
    """


    # (1) order the features form the best to the worst predictor 

    if feature_number==1:
        # prepare and order the data, (we will use data from all methods) 
        median_values = simple_models_df.groupby(["feature 1"])[value_to_use].agg(["min", sort_by, "max"])
        median_values = median_values.reset_index(drop=False)
        median_values = median_values.sort_values(sort_by)

    if feature_number==2: 
        # prepare and order the data, (we will use data from all methods) 
        value_to_use = "real_test_mae"

        # replace feature 1 with feasture 2 and concatenate, 
        #.        to accumulate data on all features in all combinaitons
        simple_models_df2 = simple_models_df.copy()
        simple_models_df2.loc[:,"feature 1"] = simple_models_df2.loc[:,"feature 2"]
        simple_models_df_all = pd.concat([simple_models_df, simple_models_df2], axis=0)

        # now use groupby to get min/mean/max for each feature, and to order the features
        median_values = simple_models_df_all.groupby(["feature 1"])[value_to_use].agg(["min", sort_by, "max"])
        median_values = median_values.reset_index(drop=False)
        median_values = median_values.sort_values(sort_by)


    # (2) prepare data for return,
    ordered_list_of_features = median_values.loc[:, "feature 1"]
    r_filter = ordered_list_of_features.str.contains("baseline", flags=re.IGNORECASE)==False
    ordered_list_of_features = ordered_list_of_features.loc[r_filter]
    ordered_list_of_features = ordered_list_of_features.reset_index(drop=True)
    
    # (2b)
    if verbose==True:
        print(f"{len(ordered_list_of_features)} categories were evaluated")
    
    
    # (3) display the plot, for evaluation, 

    # ---- plot ----    

    # make plot with trenline for each method, 
    fig, ax      = plt.subplots(figsize=(18,4))
    fig.suptitle(plot_title, fontsize=25, color="steelblue")

    # shade results on plot
    ax.fill_between(
        np.arange(median_values.shape[0]), 
        median_values.loc[:,"min"].values, 
        median_values.loc[:,"max"].values, 
        alpha=0.2)

    # add line with mean or median values
    ax.plot(median_values.loc[:, sort_by].values, color="forestgreen")

    # add horizonatal line with baseline, 
    find_baseline  = (median_values.loc[:,"feature 1"].str.contains("baseline", flags=re.IGNORECASE)) & (median_values.loc[:,"feature 1"].str.contains(sort_by))
    baseline_level = median_values.loc[find_baseline,:]
    baseline_level = baseline_level.loc[:, sort_by].values[0]
    # ....
    ax.axhline(y=baseline_level, color="red", ls="--", label="baseline")


    # ---- aestetics ----    

    # Add ticks,
    ax.set_xticks(np.arange(median_values.shape[0]))
    ax.set_xticklabels(median_values.loc[:, "feature 1"].astype("str").tolist(), fontsize=10, color="red")

    # Format ticks,
    ax.tick_params(axis='x', colors='black', direction='out', length=4, width=2, rotation=80) # tick only
    ax.tick_params(axis='y', colors='black', direction='out', length=4, width=2) # tick only    
    ax.yaxis.set_ticks_position('left')# shows only that
    ax.xaxis.set_ticks_position('bottom')# shows only that

    # tick label fontsize
    ax.tick_params(axis='both',labelsize=10)

    # Remove ticks, and axes that you dot'n want, format the other ones,
    ax.spines['top'].set_visible(False) # remove ...
    ax.spines['right'].set_visible(False) # remove ...  
    ax.spines['bottom'].set_linewidth(2) # x axis width
    ax.spines['left'].set_linewidth(2) # y axis width 

    # Add vertical lines from grid,
    ax.xaxis.grid(color='grey', linestyle='--', linewidth=0.5) # horizontal lines
    ax.yaxis.grid(color='grey', linestyle='--', linewidth=0.5) # horizontal lines

    # add legend, and xy, labels
    ax.set_xlabel("ordered features", fontsize=20)
    ax.set_ylabel("MAE", fontsize=20)
    ax.legend(loc=2)
    ax.set_ylim(y_limit[0],y_limit[1])

    # ---- final corrections -----

    # Add legends and display the plot,
    plt.subplots_adjust(top=0.8)


    # (4) retunr, 
    return ordered_list_of_features   

    """Caution there is a confilct if I place plt.show(); before return, or opposite in the fucntion"""



    
    
    
    
    
    
# Function, .................................................................................    
    
def show_best_models(
    simple_models_df,
    sort_by = "real_test_mae",
    aggreagate_by = "mean",
    N_examples = 3
):
    """
        ..........................................................................................
        the function use results from many models, to print basic informaiton 
        on top N requested models,
        ..........................................................................................
        
        simple_models_df          : dataframe, unordered models, 
                                    created with different number of features,       
        sort_by                   : str, {real_test_mae, real_train_mae, test_mae, train_mae} 
                                    error results, used to order the models,
        aggreagate_by             : str, {"mean", "meadn"} 
                                    I run models, several time, using different combinations,
                                    of rows in test/train data, that function aggregates values 
                                    from these models,
        N_examples                : how many top performing models to show, in printed summary,                                
    """
    
    # ... to start with
    simple_models_df = simple_models_df.copy()
    
    # ... constants, 
    cols_to_present  = ["method",'feature names']
    cols_to_take     = [ sort_by, "feature nr", "best_alpha", "best_l1"] 

    #(simple_models_df.loc[:,"ID"]==0).sum()
    # ... find results for each combination of feature/method
    agg_for_method_feature_comb = simple_models_df.groupby(["method", 'feature names'])[cols_to_take].agg([aggreagate_by])
    agg_for_method_feature_comb = agg_for_method_feature_comb.reset_index(drop=False)
    agg_for_method_feature_comb.columns = ["method", "Features", sort_by, "Feature_nr", "best_alpha", "best_l1"]
    sorted_agg_for_method_feature_comb = agg_for_method_feature_comb.sort_values(sort_by)
    sorted_agg_for_method_feature_comb = sorted_agg_for_method_feature_comb.reset_index(drop=True)

    # ... display, 
    for i in range(N_examples):
        print(f"\ntop perfoming model nr {i+1}")
        print(f"...............................")
        print(sorted_agg_for_method_feature_comb.iloc[i, :])
    print("done")




    
    
    




# Function, .............................................................

def fit_and_test_models_with_different_complexity(
    X_model, 
    y_model,
    X_validation, 
    y_validation,
    list_of_ordered_features,
    number_of_random_states=1,
    model_complexity=[1],
    test_size=0.2,
    verbose=True
    ):
    """
        ..........................................................................................
        the function fits, and test predictions on several models, 
        using list with models with different complexity. The analyis is reapeated n time (number_of_random_states)
        with different combinaiton of samples (rows) in train/test X,y subsets
        ..........................................................................................
        
        number_of_random_states   : int, >=1, number of time, the entire analysis 
                                    is rerapeated with different combination of rows in 
                                    train and in test data sets,
                                    
        model_complexity          : list(int), how many columns is being used to build models, 
                                    subsequelty used to evaklueat each featurew effect on MAE/MSE
                                    Currently, supported only 1 or 2, 
                                    Important - IT MUST BE A LIST, even with one integer !
                                    
                                    
                                    
    """


    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    # ....
    from sklearn.dummy import DummyRegressor
    from sklearn.linear_model import LinearRegression, HuberRegressor, SGDRegressor
    from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV # builtin cross-validation, test many alphas, return best one, 
    # .....
    from sklearn.metrics import mean_absolute_error as MAE
    from sklearn.metrics import mean_squared_error as MSE

    # ignore warning, informing that scaller chnages unit8 and int into float64, 
    import warnings
    from sklearn.exceptions import DataConversionWarning
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    # .....
    from  warnings import simplefilter
    from sklearn.exceptions import ConvergenceWarning
    simplefilter("ignore", category=ConvergenceWarning)
    # when alpha is too small, but it happen only 2-3 times, with binary variables, so I will ignore that, 


    #### silo for the results,
    results      = [] 
    
    
    #### data
    
    # train/test data for the models (caution these were also used to select features)
    X_model      = X_model.copy()
    y_model      = y_model.copy()
    
    # validation datasets, ever used before, even for EDA on data, 
    X_validation      = X_validation.copy()
    y_validation      = y_validation.copy()
    
    
    

    #### Function Helper, 
    def real_MAE(y_te_s, predicted_y_s):
        """ calculates MAE for y values that werter transfomed on log scale, """
        
        y_te_s=y_te_s.copy()
        predicted_y_s=predicted_y_s.copy()
        
        # use np.e**<value>-1 to get real predicted and tater values, 
        real_y_te        = np.abs(((np.e**y_te_s)-1).astype("int"))
        real_predicted_y = np.abs(((np.e**predicted_y_s)-1).astype("int"))

        # calulate mae,
        mae = MAE(real_y_te,  real_predicted_y)

        # return,
        return mae


    #### Function Helper, 
    def real_MSE(y_te_s, predicted_y_s):
        """ calculates MSE for y values that werter transfomed on log scale, """

        y_te_s=y_te_s.copy()
        predicted_y_s=predicted_y_s.copy()
        
        # use np.e**<value>-1 to get real predicted and tater values, 
        real_y_te        = np.abs(((np.e**y_te_s)-1).astype("int"))
        real_predicted_y = np.abs(((np.e**predicted_y_s)-1).astype("int"))

        # calulate mae,
        mse = MSE(real_y_te,  real_predicted_y)

        # return,
        return mse



    #### Train all models, and baseline, calulate mae/mse and collect the results, 
    for random_state in range(number_of_random_states):


        # data preparation,

        # ... divide df's,
        X_tr, X_te, y_tr, y_te = train_test_split(
            X_model, 
            y_model, 
            test_size=test_size, 
            random_state=random_state)

        # ... min, max y values for clipping, predicitons,
        min_y = y_tr.min()
        max_y = y_tr.max()

        # ... Info,
        if verbose==True:
            print("--------------------------------------------")
            print(f"random state: {random_state}")
            print("--------------------------------------------")


        # Baseline,
        """ Baseline is calculated only once, for each random state """

        baseline_strategy = ["mean", "median"]
        id_numbers        = list(range(len(baseline_strategy)))
        for bs, id_for_groupby in zip(baseline_strategy, id_numbers):

            # ... fit baseline model, on  full data,  
            base = DummyRegressor(strategy=bs)
            base.fit(X_tr, y_tr)

            # Predict y values, using the baseline, and collect the results,
            results.append({
                            'method'            : f"baseline {bs}",
                            'meodel_complexity' : model_complexity,
                            'feature nr'        : len(list(X_tr.columns)),
                            'feature names'     : f"baseline {bs}",    # because it doents matter,
                            'random_state'      : random_state,
                             "ID"               : id_for_groupby,

                            # ......
                            'train_mae'      : MAE(y_tr,        base.predict(X_tr)),
                            'test_mae'       : MAE(y_te,        base.predict(X_te)),
                            'real_train_mae' : real_MAE(y_tr,   base.predict(X_tr)),
                            'real_test_mae'  : real_MAE(y_te,   base.predict(X_te)),

                            # ......
                            'train_mse'      : MSE(y_tr,        base.predict(X_tr)),
                            'test_mse'       : MSE(y_te,        base.predict(X_te)),
                            'real_train_mse' : real_MSE(y_tr,   base.predict(X_tr)),
                            'real_test_mse'  : real_MSE(y_te,   base.predict(X_te)),
                
                            # ......
                            'validation_mae'       : MAE(y_validation,        base.predict(X_validation)),
                            'validation_mse'       : MSE(y_validation,        base.predict(X_validation)),
                            'real_validation_mae'  : real_MAE(y_validation,   base.predict(X_validation)),
                            'real_validation_mse'  : real_MSE(y_validation,   base.predict(X_validation)),
                
                            # ....
                            'best_alpha': np.nan,
                            "best_l1": np.nan,

                            # .... and because t was easier to do that, 
                            'feature 1': f"baseline {bs}",
                            'feature 2': f"baseline {bs}",
                            'df_shape' : X_tr.shape,
                
                            # .... new columns, 
                            "arr y_test": y_te,   
                            "arr predicted_y_test": base.predict(X_te),
                
                            # .... new columns, 
                            "arr y_train": y_tr,   
                            "arr predicted_y_train": base.predict(X_tr),
                
                            # .... new columns, 
                            "arr y_validation": y_validation,   
                            "arr predicted_y_validation": base.predict(X_validation)
                
                })

        # for later on,
        id_for_groupby = len(baseline_strategy)
  
        # loop, over each feature (complexity==1) or feature combination (complexity==2)
        for i, feature_nr in enumerate(model_complexity):

            
            # (1) prepare df_subset with selected feature/s, for both train and test data
            
            # ... find column names to slice out
            col_names_to_use = list_of_ordered_features[0:int(feature_nr)] # feature_nr stzarts at 1, so its ok to slice !
            
            # ... subset columns, 
            X_tr_subset = X_tr.loc[:,col_names_to_use]
            X_te_subset = X_te.loc[:,col_names_to_use]
            X_validation_subset = X_validation.loc[:,col_names_to_use]
            
            # ... some names for uniform table, so old fun ctions work,
            feature_1 = f"{feature_nr} features used"
            feature_2 = f"{feature_nr} features used"
              
            # ... Info,
            if verbose==True:
                if feature_nr%20==0:
                    print(f"In progress :: feature nr: {feature_nr}; adding feature :: {col_names_to_use[feature_nr-1]}")
 
            # (2) transform the data,                

            # ... tranform data subsets,
            my_transformer     = PandasPreprocessorHousePrices(0.9) 
            X_tr_subset_transf = my_transformer.fit_transform(X_tr_subset)
            X_te_subset_transf = my_transformer.transform(X_te_subset)
            X_validation_subset_transf = my_transformer.transform(X_validation_subset)

            # ... Standardize features for some models,
            scaler                      = StandardScaler()
            X_tr_subset_transf_rescaled = scaler.fit_transform(X_tr_subset_transf) # calculate meas, SD's
            X_te_subset_transf_rescaled = scaler.transform(X_te_subset_transf)     # standarize
            X_validation_subset_transf_rescaled = scaler.transform(X_validation_subset_transf)     # standarize

            
            
            # (3) instanciate selected models, and decide on hypeparameters for grid search, 

            # ...
            lr     = LinearRegression()
            huber  = HuberRegressor(epsilon=1.2)

            # ... 
            lr_sgd = SGDRegressor(
                loss='squared_loss',           #  Cost function
                penalty='none',                # Add a penalty term?, no not in this case, 
                max_iter=10000,                # Number of iterations
                random_state=random_state,     # The implementation shuffles the data, the we will have always the same reult. 
                tol=1e-3                       # Tolerance for improvement (stop SGD once loss is below)
            )

            # .....
            alphas  = np.logspace(-1, 4, num=20)  
            ridgeCV = RidgeCV(alphas=alphas)   # Ridge with built in cross-validation 
            lassoCV = LassoCV(alphas=alphas, max_iter=10000, cv=3) # cv, determines, cv procedure, 3-fold, 

            # .....
            l1_ratios = np.linspace(0.01, 1, num=10)
            elasticCV   = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratios, cv=3)


            # (4) fit each model and collect the results,  

            for model, model_name in zip(
                    [lr, huber, lr_sgd, ridgeCV, lassoCV, elasticCV], 
                    ["lr", "huber", "lr_sgd", "ridgeCV", "lassoCV", "elasticCV"]
                ):
                
                # ... COUNTER - id number that will allo to gropupby methods without any problems
                id_for_groupby +=1
                
                # .... fit
                model.fit(X_tr_subset_transf_rescaled, y_tr)

                # .... Predict y values, using the model,
                predicted_y_tr = model.predict(X_tr_subset_transf_rescaled).clip(min=min_y, max=max_y)
                predicted_y_te = model.predict(X_te_subset_transf_rescaled).clip(min=min_y, max=max_y)
                predicted_y_validation = model.predict(X_validation_subset_transf_rescaled).clip(min=min_y, max=max_y)
                

                # .... find best_alpha if applicable,
                if model_name=="ridgeCV" or model_name=="lassoCV" or model_name=="elasticCV":
                    best_alpha = model.alpha_
                else:
                    best_alpha      = np.nan

                # .... find best_l1 if applicable,
                if model_name=="elasticCV":
                    best_l1 = model.l1_ratio_
                else:
                    best_l1      = np.nan 

                # .... collect results,
                results.append({
                        'method'            : model_name,
                        'meodel_complexity' : feature_nr,
                        'feature nr'        : len(list(X_tr_subset.columns)),
                        'feature names'     : ", ".join(list(X_tr_subset.columns)),
                        'random_state'      : random_state,
                        "ID"                : id_for_groupby,

                        # ......
                        'train_mae'     : MAE(y_tr,   predicted_y_tr),
                        'test_mae'      : MAE(y_te,   predicted_y_te),
                        'real_train_mae': real_MAE(y_tr,   predicted_y_tr),
                        'real_test_mae' : real_MAE(y_te,   predicted_y_te),

                        # ......
                        'train_mse'     : MSE(y_tr,   predicted_y_tr),
                        'test_mse'      : MSE(y_te,   predicted_y_te),
                        'real_train_mse': real_MSE(y_tr,   predicted_y_tr),
                        'real_test_mse' : real_MSE(y_te,   predicted_y_te),

                        # ......
                        'validation_mae'        : MAE(y_validation,   predicted_y_validation),
                        'validation_mse'        : MSE(y_validation,   predicted_y_validation),
                        'real_validation_mae'   : real_MAE(y_validation,   predicted_y_validation),
                        'real_validation_mse'   : real_MSE(y_validation,   predicted_y_validation),
     
                        # ....
                        'best_alpha': best_alpha,
                        "best_l1": best_l1,

                        # .... and because t was easier to do that, 
                        'feature 1': feature_1,
                        'feature 2': feature_2,
                        'df_shape' : X_tr_subset_transf_rescaled.shape,
                    
                        # .... new columns, 
                        "arr y_test": y_te,   
                        "arr predicted_y_test": predicted_y_te,
                    
                        # .... new columns, 
                        "arr y_train": y_tr,   
                        "arr predicted_y_train": predicted_y_tr,
                    
                        # .... new columns, 
                        "arr y_validation": y_validation,   
                        "arr predicted_y_validation": predicted_y_validation
                    
                    
            })  
                
    #### return,
    return results







# Function, ................................................................................
 
def fit_and_test_models_with_different_complexity(
    X_model, 
    y_model,
    X_validation, 
    y_validation,
    EPFL_ext_test_data,
    list_of_ordered_features,
    number_of_random_states=1,
    model_complexity=[1],
    test_size=0.2,
    verbose=True
    ):
    """
        ..........................................................................................
        the function fits, and test predictions on several models, 
        using list with models with different complexity. The analyis is reapeated n time (number_of_random_states)
        with different combinaiton of samples (rows) in train/test X,y subsets
        ..........................................................................................
        
        number_of_random_states   : int, >=1, number of time, the entire analysis 
                                    is rerapeated with different combination of rows in 
                                    train and in test data sets,
                                    
        model_complexity          : list(int), how many columns is being used to build models, 
                                    subsequelty used to evaklueat each featurew effect on MAE/MSE
                                    Currently, supported only 1 or 2, 
                                    Important - IT MUST BE A LIST, even with one integer !
                                    
                                    
                                    
    """

    #### silo for the results,
    results      = [] 
    
    
    #### data
    
    # train/test data for the models (caution these were also used to select features)
    X_model      = X_model.copy()
    y_model      = y_model.copy()
    
    # validation datasets, ever used before, even for EDA on data, 
    X_validation      = X_validation.copy()
    y_validation      = y_validation.copy()
    
    
    ###### prepare EPFL_ext_test_data, for external validation,
    
    # .. save PID numbers,
    EPFL_ext_test_data = EPFL_ext_test_data.copy()
    EPFL_ext_test_data_PID = EPFL_ext_test_data.loc[:, "PID"]
    
    
    

    #### Function Helper, 
    def real_MAE(y_te_s, predicted_y_s):
        """ calculates MAE for y values that werter transfomed on log scale, """
        
        y_te_s=y_te_s.copy()
        predicted_y_s=predicted_y_s.copy()
        
        # use np.e**<value>-1 to get real predicted and tater values, 
        real_y_te        = np.abs(((np.e**y_te_s)-1).astype("int"))
        real_predicted_y = np.abs(((np.e**predicted_y_s)-1).astype("int"))

        # calulate mae,
        mae = MAE(real_y_te,  real_predicted_y)

        # return,
        return mae


    #### Function Helper, 
    def real_MSE(y_te_s, predicted_y_s):
        """ calculates MSE for y values that werter transfomed on log scale, """

        y_te_s=y_te_s.copy()
        predicted_y_s=predicted_y_s.copy()
        
        # use np.e**<value>-1 to get real predicted and tater values, 
        real_y_te        = np.abs(((np.e**y_te_s)-1).astype("int"))
        real_predicted_y = np.abs(((np.e**predicted_y_s)-1).astype("int"))

        # calulate mae,
        mse = MSE(real_y_te,  real_predicted_y)

        # return,
        return mse



    #### Train all models, and baseline, calulate mae/mse and collect the results, 
    for random_state in range(number_of_random_states):


        # data preparation,

        # ... divide df's,
        X_tr, X_te, y_tr, y_te = train_test_split(
            X_model, 
            y_model, 
            test_size=test_size, 
            random_state=random_state)

        # ... min, max y values for clipping, predicitons,
        min_y = y_tr.min()
        max_y = y_tr.max()

        # ... Info,
        if verbose==True:
            print("--------------------------------------------")
            print(f"random state: {random_state}")
            print("--------------------------------------------")


        # Baseline,
        """ Baseline is calculated only once, for each random state """

        baseline_strategy = ["mean", "median"]
        id_numbers        = list(range(len(baseline_strategy)))
        for bs, id_for_groupby in zip(baseline_strategy, id_numbers):

            # ... fit baseline model, on  full data,  
            base = DummyRegressor(strategy=bs)
            base.fit(X_tr, y_tr)

            # Predict y values, using the baseline, and collect the results,
            results.append({
                            'method'            : f"baseline {bs}",
                            'meodel_complexity' : model_complexity,
                            'feature nr'        : len(list(X_tr.columns)),
                            'feature names'     : f"baseline {bs}",    # because it doents matter,
                            'random_state'      : random_state,
                             "ID"               : id_for_groupby,

                            # ......
                            'train_mae'      : MAE(y_tr,        base.predict(X_tr)),
                            'test_mae'       : MAE(y_te,        base.predict(X_te)),
                            'real_train_mae' : real_MAE(y_tr,   base.predict(X_tr)),
                            'real_test_mae'  : real_MAE(y_te,   base.predict(X_te)),

                            # ......
                            'train_mse'      : MSE(y_tr,        base.predict(X_tr)),
                            'test_mse'       : MSE(y_te,        base.predict(X_te)),
                            'real_train_mse' : real_MSE(y_tr,   base.predict(X_tr)),
                            'real_test_mse'  : real_MSE(y_te,   base.predict(X_te)),
                
                            # ......
                            'validation_mae'       : MAE(y_validation,        base.predict(X_validation)),
                            'validation_mse'       : MSE(y_validation,        base.predict(X_validation)),
                            'real_validation_mae'  : real_MAE(y_validation,   base.predict(X_validation)),
                            'real_validation_mse'  : real_MSE(y_validation,   base.predict(X_validation)),
                
                            # ....
                            'best_alpha': np.nan,
                            "best_l1": np.nan,

                            # .... and because t was easier to do that, 
                            'feature 1': f"baseline {bs}",
                            'feature 2': f"baseline {bs}",
                            'df_shape' : X_tr.shape,
                
                            # .... new columns, 
                            "arr y_test": y_te,   
                            "arr predicted_y_test": base.predict(X_te),
                
                            # .... new columns, 
                            "arr y_train": y_tr,   
                            "arr predicted_y_train": base.predict(X_tr),
                
                            # .... new columns, 
                            "arr y_validation": y_validation,   
                            "arr predicted_y_validation": base.predict(X_validation),
                
                            ### EPFL_ext_test_data - only predictions and PID
                            "arr EPFL_ext_test_data_PID": np.nan,
                            "arr predicted_y_EPFL_ext_test_data": np.nan 

                })

        # for later on,
        id_for_groupby = len(baseline_strategy)
  
        # loop, over each feature (complexity==1) or feature combination (complexity==2)
        for i, feature_nr in enumerate(model_complexity):

            
            # (1) prepare df_subset with selected feature/s, for both train and test data
            
            # ... find column names to slice out
            col_names_to_use = list_of_ordered_features[0:int(feature_nr)] # feature_nr stzarts at 1, so its ok to slice !
            
            # ... subset columns, 
            X_tr_subset = X_tr.loc[:,col_names_to_use]
            X_te_subset = X_te.loc[:,col_names_to_use]
            X_validation_subset = X_validation.loc[:,col_names_to_use]
            EPFL_ext_test_data_subset = EPFL_ext_test_data.loc[:,col_names_to_use]
            
            # ... some names for uniform table, so old fun ctions work,
            feature_1 = f"{feature_nr} features used"
            feature_2 = f"{feature_nr} features used"
              
            # ... Info,
            if verbose==True:
                if feature_nr%20==0:
                    print(f"In progress :: feature nr: {feature_nr}; adding feature :: {col_names_to_use[feature_nr-1]}")
 
            # (2) transform the data,                

            # ... tranform data subsets,
            my_transformer     = PandasPreprocessorHousePrices(0.9) 
            X_tr_subset_transf = my_transformer.fit_transform(X_tr_subset)
            X_te_subset_transf = my_transformer.transform(X_te_subset)
            X_validation_subset_transf = my_transformer.transform(X_validation_subset)
            EPFL_ext_test_data_subset_transf = my_transformer.transform(EPFL_ext_test_data_subset)

            # ... Standardize features for some models,
            scaler                      = StandardScaler()
            X_tr_subset_transf_rescaled = scaler.fit_transform(X_tr_subset_transf) # calculate meas, SD's
            X_te_subset_transf_rescaled = scaler.transform(X_te_subset_transf)     # standarize
            X_validation_subset_transf_rescaled = scaler.transform(X_validation_subset_transf)     # standarize
            EPFL_ext_test_data_subset_transf_rescaled = scaler.transform(EPFL_ext_test_data_subset_transf)
            
            
            # (3) instanciate selected models, and decide on hypeparameters for grid search, 

            # ...
            lr     = LinearRegression()
            huber  = HuberRegressor(epsilon=1.2)

            # ... 
            lr_sgd = SGDRegressor(
                loss='squared_loss',           #  Cost function
                penalty='none',                # Add a penalty term?, no not in this case, 
                max_iter=10000,                # Number of iterations
                random_state=random_state,     # The implementation shuffles the data, the we will have always the same reult. 
                tol=1e-3                       # Tolerance for improvement (stop SGD once loss is below)
            )

            # .....
            alphas  = np.logspace(-1, 4, num=20)  
            ridgeCV = RidgeCV(alphas=alphas)   # Ridge with built in cross-validation 
            lassoCV = LassoCV(alphas=alphas, max_iter=10000, cv=3) # cv, determines, cv procedure, 3-fold, 

            # .....
            l1_ratios = np.linspace(0.01, 1, num=10)
            elasticCV   = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratios, cv=3)


            # (4) fit each model and collect the results,  

            for model, model_name in zip(
                    [lr, huber, lr_sgd, ridgeCV, lassoCV, elasticCV], 
                    ["lr", "huber", "lr_sgd", "ridgeCV", "lassoCV", "elasticCV"]
                ):
                
                # ... COUNTER - id number that will allo to gropupby methods without any problems
                id_for_groupby +=1
                
                # .... fit
                model.fit(X_tr_subset_transf_rescaled, y_tr)

                # .... Predict y values, using the model,
                predicted_y_tr = model.predict(X_tr_subset_transf_rescaled).clip(min=min_y, max=max_y)
                predicted_y_te = model.predict(X_te_subset_transf_rescaled).clip(min=min_y, max=max_y)
                predicted_y_validation = model.predict(X_validation_subset_transf_rescaled).clip(min=min_y, max=max_y)
                predicted_y_EPFL_ext_test_data = model.predict(EPFL_ext_test_data_subset_transf_rescaled).clip(min=min_y, max=max_y)
 
                # .... find best_alpha if applicable,
                if model_name=="ridgeCV" or model_name=="lassoCV" or model_name=="elasticCV":
                    best_alpha = model.alpha_
                else:
                    best_alpha      = np.nan

                # .... find best_l1 if applicable,
                if model_name=="elasticCV":
                    best_l1 = model.l1_ratio_
                else:
                    best_l1      = np.nan 

                # .... collect results,
                results.append({
                        'method'            : model_name,
                        'meodel_complexity' : feature_nr,
                        'feature nr'        : len(list(X_tr_subset.columns)),
                        'feature names'     : ", ".join(list(X_tr_subset.columns)),
                        'random_state'      : random_state,
                        "ID"                : id_for_groupby,

                        # ......
                        'train_mae'     : MAE(y_tr,   predicted_y_tr),
                        'test_mae'      : MAE(y_te,   predicted_y_te),
                        'real_train_mae': real_MAE(y_tr,   predicted_y_tr),
                        'real_test_mae' : real_MAE(y_te,   predicted_y_te),

                        # ......
                        'train_mse'     : MSE(y_tr,   predicted_y_tr),
                        'test_mse'      : MSE(y_te,   predicted_y_te),
                        'real_train_mse': real_MSE(y_tr,   predicted_y_tr),
                        'real_test_mse' : real_MSE(y_te,   predicted_y_te),

                        # ......
                        'validation_mae'        : MAE(y_validation,   predicted_y_validation),
                        'validation_mse'        : MSE(y_validation,   predicted_y_validation),
                        'real_validation_mae'   : real_MAE(y_validation,   predicted_y_validation),
                        'real_validation_mse'   : real_MSE(y_validation,   predicted_y_validation),
     
                        # ....
                        'best_alpha': best_alpha,
                        "best_l1": best_l1,

                        # .... and because t was easier to do that, 
                        'feature 1': feature_1,
                        'feature 2': feature_2,
                        'df_shape' : X_tr_subset_transf_rescaled.shape,
                    
                        # .... new columns, 
                        "arr y_test": y_te,   
                        "arr predicted_y_test": predicted_y_te,
                    
                        # .... new columns, 
                        "arr y_train": y_tr,   
                        "arr predicted_y_train": predicted_y_tr,
                    
                        # .... new columns, 
                        "arr y_validation": y_validation,   
                        "arr predicted_y_validation": predicted_y_validation,
                    
                        ### EPFL_ext_test_data - only predictions and PID
                        "arr EPFL_ext_test_data_PID": EPFL_ext_test_data_PID.values,
                        "arr predicted_y_EPFL_ext_test_data": predicted_y_EPFL_ext_test_data                    

                    
            })  
                
    #### return,
    return results






# Function, .....................................................................................
 
def plot_error_for_models_with_increasing_feature_number(
    model_evaluation_df,
    value_to_use        = "real_test_mae",
    display_on_plot     = "median",
    fig_title           = "Title",
    ylimit_fixed        = True,
    upper_y_limit       = 65000,
    xticklabels_sparse  = True
    ): 

    """
        ..........................................................................................
        the function creates plot with trendlines showing error scores calulated 
        for different models, created with different number of features, 
        Values are sorted and agregated, by model name, and feature number, 
        
         - Important -  
        making this funtion, I asssumed that the features were ordered from best to worst predictor, 
        and that models with the same number of features have exactly the same features in it,
        ..........................................................................................
        
        model_evaluation_df       : dataframe, unordered models, 
                                    created with different number of features,       
        value_to_use              : str, {real_test_mae, real_train_mae, test_mae, train_mae} 
                                    error results, used to order the models,
        display_on_plot           : str, {"mean", "meadn"} - value used to create trendlines,
                                    I run models, several time, using different combinations,
                                    of rows in test/train data, that function aggregates values 
                                    from these models,
        ylimit_fixed              : bool, if True, upper_y_limit is fixed,
        x_limit                   : int, top value on plot,
        upper_y_limit             : int, top value on plot,    
        
        
        
    """    
    
    
    # copy df, 
    model_evaluation_df = model_evaluation_df.copy()


    # get data, to display,

    # .. extract and aggreagate data,
    models_results = model_evaluation_df.groupby(["method", 'feature nr'])[value_to_use].agg([display_on_plot])
    models_results = models_results.reset_index(drop=False)

    # ... results for trendline, no baselines 
    notbaseline    = (models_results.method.str.contains("baseline")==False)
    models_results_nobaseline = models_results.loc[notbaseline,:]

    # baseline results only,
    baseline_results_pos = models_results.method.str.contains(f"baseline {display_on_plot}")
    results_baseline = models_results.loc[baseline_results_pos,:]
    baseline_value   = results_baseline.loc[[True],display_on_plot].values[0]

    # .. find all method names
    method_names = pd.Series(models_results.method.unique())
    notbaseline  = (method_names.str.contains("baseline")==False)
    method_names = method_names[notbaseline].values.tolist()

    

    # plot trendlines, 

    # .. fig, axes, 
    fig, ax    = plt.subplots(figsize=(8,6))
    fig.suptitle(fig_title, fontsize=25, color="black")

    # some fixed values
    linestyles = ["solid", "dashed", "dashdot", "solid", "dashed", "dashdot" ]
    # more on linestyles https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
    
    
    # .. add trendlines with mediants from each method, 
    for i, mt in enumerate(method_names):

        # ... select data for a trendline,
        row_res_for_one_mt    = models_results_nobaseline.method.str.contains(f"^{mt}$")
        one_method_results    = models_results_nobaseline.loc[row_res_for_one_mt,:]

        # .... plot trendline, 
        ax.plot(
            np.arange(1,one_method_results.shape[0]+1), 
            one_method_results.loc[:, display_on_plot].values,
            label=mt, lw=2, ls=linestyles[i]
        )

        # .... set y limit for plot
        if ylimit_fixed==False:
            if one_method_results.loc[:, display_on_plot].values.max() > upper_y_limit:
                upper_y_limit = one_method_results.loc[:, display_on_plot].values.max() 


    # add line with baseline,             
    ax.axhline(y=baseline_value, color="dimgrey", ls="-", lw=2, label="baseline")

    # set limits, for plot, 
    ax.set_ylim(0,upper_y_limit)

    # Format ticks, axes and grids,

    # set xtick labels and postions, 
    xtick_labels = one_method_results.loc[:,'feature nr'].values.tolist()

    if xticklabels_sparse==False:
        # Add all possible ticks,
        ax.set_xticks(np.arange(1,len(xtick_labels)+1))
        ax.set_xticklabels(xtick_labels, fontsize=8)
    else:
        xtick_labels = np.arange(0,len(xtick_labels)+2, 5)
        ax.set_xticks(xtick_labels)
        ax.set_xticklabels(xtick_labels, fontsize=15)        

    # Format ticks,
    ax.tick_params(axis='x', colors='black', direction='out', length=4, width=2) # tick only
    ax.tick_params(axis='y', colors='black', direction='out', length=4, width=2) # tick only    
    ax.yaxis.set_ticks_position('left')# shows only that
    ax.xaxis.set_ticks_position('bottom')# shows only that

    # tick label fontsize
    ax.tick_params(axis='y',labelsize=15)

    # Remove ticks, and axes that you dot'n want, format the other ones,
    ax.spines['top'].set_visible(False) # remove ...
    ax.spines['right'].set_visible(False) # remove ...  
    ax.spines['bottom'].set_linewidth(2) # x axis width
    ax.spines['left'].set_linewidth(2) # y axis width 

    # Add vertical lines from grid,
    ax.xaxis.grid(color='grey', linestyle=':', linewidth=0.5) # horizontal lines
    ax.yaxis.grid(color='grey', linestyle=':', linewidth=0.5) # horizontal lines

    # add legend, and xy, labels
    ax.set_xlabel("\nNumber of Features used by each Model\nthe features were ordered in step 2 (1-79)\n", fontsize=20)
    ax.set_ylabel("\nMAE (USD)\n", fontsize=20)
    legend= ax.legend(
        scatterpoints=1, 
        loc = 'right', 
        frameon=False, 
        ncol=1, 
        title="METHOD", 
        framealpha=1,
        fontsize=15,
         bbox_to_anchor=(1.3, 0.6)
    )
    plt.setp(legend.get_title(),fontsize=15) # legeng title fontsize

    # Add legends and display the plot,
    plt.subplots_adjust(top=0.7)
    plt.show();






# Function, .....................................................................................

def order_models_based_on_method_feastureName_and_performance(
    model_evaluation_results_df,
    sort_by = "real_test_mae",
    aggreagate_by = "mean"
):
    """
        ..........................................................................................
        This function takes results of multi-model evalusdation and returns the list of ordered 
        models done with different approaches, on different number of features.
        Function is used by Plot_SalePrice_with_all_predictions()
        ..........................................................................................
        
        simple_models_df          : dataframe, unordered models, 
                                    created with different number of features,       
        sort_by                   : str, {real_test_mae, real_train_mae, test_mae, train_mae} 
                                    error results, used to order the models,
        aggreagate_by             : str, {"mean", "mean"} 
                                    I run models, several time, using different combinations,
                                    of rows in test/train data, that function aggregates values 
                                    from these models,                              
    """
    
    # ... to start with
    model_evaluation_results_df = model_evaluation_results_df.copy()
    
    # ... constants, 
    cols_to_present  = ["method",'feature nr']
    cols_to_take     = [ sort_by, "best_alpha", "best_l1"] 

    #(simple_models_df.loc[:,"ID"]==0).sum()
    # ... find results for each combination of feature/method
    agg_for_method_feature_comb = model_evaluation_results_df.groupby(["method", 'feature nr'])[cols_to_take].agg([aggreagate_by])
    agg_for_method_feature_comb = agg_for_method_feature_comb.reset_index(drop=False)
    agg_for_method_feature_comb.columns = ["method", "Feature_nr", sort_by, "best_alpha", "best_l1"]
    sorted_agg_for_method_feature_comb = agg_for_method_feature_comb.sort_values(sort_by)
    sorted_agg_for_method_feature_comb = sorted_agg_for_method_feature_comb.reset_index(drop=True)

    # ... display, 
    return sorted_agg_for_method_feature_comb
    





    
    


# Function, .....................................................................................

def Plot_SalePrice_with_all_predictions(
    model_summary,
    models_to_display = list(range(1)),#ranked from 1 to n using sort by
    global_ranking = False,
    Feature_nr = 1,
    log_values = False,
    make_plot=True
):
    
    """
        ..........................................................................................
        Creates Scatter plots showing the relation between Expected (True) Sale Prices and salse 
        Prices predicted with each individual model. Each plot, presents predicted sale proces 
        with trasins , test and validation datasets, trendline created with linear regressions,
        to show general tren of redictios and trendline showing how the ideal predictions 
        shoudl look like
        ..........................................................................................
        
        model_summary             : dataframe, unordered models, 
                                    created with different number of features,       
        models_to_display         : list, with models to display, ranked from the best to the worst, 
        global_ranking            : bool, if True, ranking used on models_to_display, is applied to all 
                                    methods, and models, if false, you need to provide Feature_nr, 
                                    to select all models, build with a given feature number, and these 
                                    will be ranked separately
        Feature_nr                : int, used if global_ranking == False,
        log_values                : bool, if True, log values will be used instead of Sake Prices,
                                                                  
    """



    # First, sort methods/feature nr by model performance, 
    id_data = order_models_based_on_method_feastureName_and_performance(
        model_evaluation_results_df = model_summary,
        sort_by = "real_validation_mae",
        aggreagate_by = "mean"
    )
    
    
    # contaqiner for bonus data to return, 
    results_to_return = list()


    # .. if not useing global ranking, you shoudl use method with selected nr of features, 
    #.   I was tired, witting this function, Thus, only one feature nr combination is allowed

    if global_ranking==True:
        id_data = id_data
    else:
        r_sel = id_data.Feature_nr==Feature_nr
        id_data = id_data.loc[r_sel,:]
        id_data.reset_index(drop=True, inplace=True)

    # .. plots,
    for model_nr in models_to_display:

        # type of error to display,
        if log_values==True:
            error_values = ['test_mae', 'test_mse', 'validation_mae']
        else:
            error_values = ['real_test_mae', 'real_test_mse', 'real_validation_mae']

        #### Values, 

        # .. extract top requested models, 
        method_name = id_data.method.loc[model_nr]
        model_complexity = id_data.Feature_nr.loc[model_nr]

        # .. find them in model summary, 
        row_filter = (model_summary.loc[:,"feature nr"]==model_complexity) & (model_summary.method==method_name)



        #### get the data for plots, form model summary, 

        # ..... test data, 
        predicted_y_values = model_summary.loc[row_filter,"arr predicted_y_test"]
        expected_y_values = model_summary.loc[row_filter,"arr y_test"]
        predicted_y_values.reset_index(drop=True, inplace=True)
        expected_y_values.reset_index(drop=True, inplace=True)

        # ..... train data, 
        predicted_train_y_values = model_summary.loc[row_filter,"arr predicted_y_train"]
        expected_train_y_values = model_summary.loc[row_filter,"arr y_train"]
        predicted_train_y_values.reset_index(drop=True, inplace=True)
        expected_train_y_values.reset_index(drop=True, inplace=True)

        # ..... validation data, 
        predicted_validation_y_values = model_summary.loc[row_filter,"arr predicted_y_validation"]
        expected_validation_y_values = model_summary.loc[row_filter,"arr y_validation"]    
        predicted_validation_y_values.reset_index(drop=True, inplace=True)
        expected_validation_y_values.reset_index(drop=True, inplace=True)

        # ..... EPFL_ext_test_data 
        EPFL_ext_test_data_values = model_summary.loc[row_filter,"arr predicted_y_EPFL_ext_test_data"]
        EPFL_ext_test_data_PID_values = model_summary.loc[row_filter,"arr EPFL_ext_test_data_PID"]    
        EPFL_ext_test_data_values.reset_index(drop=True, inplace=True)
        EPFL_ext_test_data_PID_values.reset_index(drop=True, inplace=True)        
        
        

        ####  data on model to display in subplot title, 
        values_to_display = ['best_alpha', 'best_l1', error_values[0], error_values[1], error_values[2]]
        data_on_model = model_summary.loc[row_filter, values_to_display]
        data_on_model.reset_index(drop=True, inplace=True)


        #### baseline .. find and extract baseline medians, 
        baseline_rows = model_summary.method=="baseline median"
        baseline_pred = model_summary.loc[baseline_rows ,"arr predicted_y_test"]
        baseline_pred.reset_index(drop=True, inplace=True)
        baseline_values = [] 
        for r in range(baseline_pred.shape[0]):
            baseline_values.append(baseline_pred.iloc[r][0])

        # mae from baseline for test and validation ddatasets, 
        baseline_mae_test = model_summary.loc[baseline_rows ,"real_test_mae"]
        baseline_mae_test.reset_index(drop=True, inplace=True)
        baseline_mae_validation = model_summary.loc[baseline_rows ,"real_validation_mae"]
        baseline_mae_validation.reset_index(drop=True, inplace=True)



        #### plot 

        # .. fig, axes, suptitle, 
        fig, axs = plt.subplots(
            ncols=3,
            nrows=1, 
            facecolor="white",
            figsize=(18,8)
        )

        if global_ranking==True:
            plot_title = f"Model ranked as number {model_nr+1} among all methods tested\n Method: {method_name} with {model_complexity} features"
        else:
            plot_title = f"\nThree models builded with {method_name} method, with {model_complexity} features"
        
        # Figure, 
        fig.suptitle( plot_title, fontsize=30, color="black" )

        # .. subplots, 
        for snr, ax in enumerate(axs.flat):

            
            if snr+1>len(axs.flat) or snr+1>predicted_y_values.shape[0] or snr>3:
                break
            else:
                # recalculate values, to get real price instead of log,
                if log_values==True:
                    # .. test,
                    predicted_y = predicted_y_values[snr]
                    expected_y = expected_y_values[snr]

                    # .. train,
                    predicted_train_y = predicted_train_y_values[snr]
                    expected_train_y = expected_train_y_values[snr]

                    # .. validation,
                    predicted_validation_y = predicted_validation_y_values[snr]
                    expected_validation_y = expected_validation_y_values[snr]

                    # ..
                    xy_limits = (10,14)
                    err_round_to=3
                    baseline_to_plot = baseline_values[snr]

                else:
                    # .. test,
                    predicted_y = np.round(np.e**predicted_y_values[snr],0).astype(int)
                    expected_y = np.round(np.e**expected_y_values[snr],0).astype(int)

                    # ... train,
                    predicted_train_y = np.round(np.e**predicted_train_y_values[snr],0).astype(int)
                    expected_train_y = np.round(np.e**expected_train_y_values[snr],0).astype(int)

                    # .. validation, 
                    predicted_validation_y = np.round(np.e**predicted_validation_y_values[snr],0).astype(int)
                    expected_validation_y = np.round(np.e**expected_validation_y_values[snr],0).astype(int)

                    # .. EPFL_ext_test_data
                    EPFL_ext_test_data = np.e**EPFL_ext_test_data_values[snr]
                    EPFL_ext_test_data_PID = EPFL_ext_test_data_PID_values[snr] 

                    # ..
                    xy_limits = (0,800000)
                    err_round_to=0
                    baseline_to_plot = np.round(np.e**baseline_values[snr], 0).astype(int)

                    
                # .. EPFL_ext_test_data - returned only in $ values, no rounding, 
                EPFL_ext_test_data = np.e**EPFL_ext_test_data_values[snr]
                EPFL_ext_test_data_PID = EPFL_ext_test_data_PID_values[snr] 
   
                # train data, 
                ax.scatter(
                    y=predicted_train_y,
                    x=expected_train_y,
                    color="grey",
                    alpha=0.5,
                    s=60,
                    marker="o",
                    label="Train data"
                )

                # test data,
                ax.scatter(
                    y=predicted_y,
                    x=expected_y,
                    color="blue",
                    alpha=0.7,
                    s=30,
                    label="Test data"
                )

                # validation data,
                ax.scatter(
                    y=predicted_validation_y,
                    x=expected_validation_y,
                    color="orange",
                    marker="*",
                    alpha=0.8,
                    s=20,
                    label="Validation data"
                )

                # subplot title,
                tmae = f"Model MAE    = {np.round(data_on_model.iloc[snr, 2], err_round_to)}"
                vmae = f"Model MAE    = {np.round(data_on_model.iloc[snr, 4], err_round_to)}"
                btmae= f"Baseline MAE = {np.round(baseline_mae_test.iloc[snr], err_round_to)}"
                bvmae= f"Baseline MAE = {np.round(baseline_mae_validation.iloc[snr], err_round_to)}"
                # .....
                subplot_title = f"""
                Test Data\n{tmae}\n{btmae}\n
                Validation Data\n{vmae}\n{bvmae}\n\n"""   
                # .....
                ax.set_title(subplot_title, fontsize=12, color="steelblue", ha="left")


                #### BONUS PART - Build list wiht some results to return, for simple plot, 
                results_to_return.append({
                    "method" : method_name,
                    "feature_nr": model_complexity, 
                    "model_rank": model_nr,
                    "model with test data MAE" : data_on_model.iloc[snr, 2], 
                    "model with validation data MAE" : data_on_model.iloc[snr, 4],
                    "Baseline with test data MAE" : baseline_mae_test.iloc[snr],
                    "Baseline with validation data MAE" : baseline_mae_validation.iloc[snr],
                    "EPFL_ext_test_data": EPFL_ext_test_data,
                    "EPFL_ext_test_data_PID": EPFL_ext_test_data_PID
                })
                    
                # add lines presenting ideal match and regression line on the prediction,

                # ... correlations,
                pearson_rho = np.round(stats.pearsonr(
                    predicted_y, 
                    expected_y)[0], 3)

                # ... Compute a least-squares regression for two sets of measurements,
                xdata = np.linspace(0,10000000,100)
                LR_slope, LR_intercept, LR_r_value, LR_p_value, LR_std_err = stats.linregress(
                    expected_train_y,
                    predicted_train_y)
                y_data = (xdata*LR_slope)+LR_intercept

                # ... plot ideal and correlation lines,
                ax.plot(xdata, xdata, zorder=8, color="black", lw=1, ls="--", label="LR - Ideal Predictions")
                ax.plot(xdata, y_data, zorder=10, color="dimgrey", lw=3, ls="--", label="LR - Model")

                # ... baseline,
                ax.axhline(baseline_to_plot, label="median baseline")


                # axes description,
                ax.set(
                    ylim= xy_limits, 
                    xlim= xy_limits,
                )
                # ...
                ax.set_ylabel("Predicted Sale Price (USD)",fontsize=20)
                ax.set_xlabel("Expected Sale Price (USD)",fontsize=20)
                # ...
                ax.xaxis.set_major_locator(plt.MaxNLocator(3))
                ax.yaxis.set_major_locator(plt.MaxNLocator(3))
                sns.despine()

                # legened
                ax.legend(frameon=False, fontsize=12, loc=2, bbox_to_anchor=(0, 1.45))

        fig.tight_layout()   
        fig.subplots_adjust(top=0.6)
        
        if make_plot==False:
            fig_to_dump = fig
        
    # finally, return bonus data,
    return results_to_return





# Function, .......................................................................... 

def get_df_dtypes(*, df, break_at=None):
    """
        this nfucntion will print out, 
        column name, dtype and mean value for it, 
    """
    for i,j in enumerate(df.dtypes): 
        if break_at==None:
            print(f'{i}, {df.columns[i]}, dtpye = {j}, mean={df.iloc[:,i].mean()}')
        else:
            if i==break_at: break
            else:
                print(f'{i}, {df.columns[i]}, dtpye = {j}, mean={df.iloc[:,i].mean()}')
    print("\n")






# Function, ..................................................................................

def test_outlier_removal_method(
    data_df,
    continuous_features,
    zscore_cutoff=2, 
    include_zeros=True):
    """
        .........................................................................
        With this function
        .........................................................................
        
        + I ADDED RANDOM GAUSSIAN NOISE TO POINTS TO SEE THEM ALL ON A SCATTER PLOT,

        + I ADDED MEAN VALIUE AND POTENTIAL Z-.SCORE THAT COULD 
          BE USED AT CUTOFF TO FILTER OUT OUTLIERS, 

        + NUMBER OF DATA POINTS WITH NON-MISSING DATA AND POINTS THAT WOUDL 
          BE REMOVED IN CASE THAT FILTER WOUDFL BE USED, WERE CALULATED 
          AND DIPLAYED IN TITLE OF EACH SUBPLOT,
    """

    # work on copy, 
    data_df = data_df.copy()

    # Figure,
    fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(12, 14), facecolor="white")
    fig.suptitle("""Continuous features - I added random noise to x,y axes to each point
                 \nThis plot was created only to see whether there are separated clusters of datapoints
                 \nand how removing outliers with z-score may affect these points """, fontsize=20)

    # Subplots,
    for i, ax in enumerate(axs.flat):
        if i+1 > len(continuous_features): 
            break

        # Prepare y values, by addint a bit of noise for scatter plot 
        #.        - so i can see how many points is everywhere
        y_val = data_df[continuous_features[i]].dropna().values
        noise = np.random.normal(loc=0, scale=np.std(y_val), size=y_val.shape)
        
        y_val_log = np.log1p(data_df[continuous_features[i]].dropna().values)
        small_noise = np.random.normal(loc=0, scale=np.std(y_val_log)/20, size=y_val_log.shape)
        
        # Scatter plot
        ax.scatter(x= y_val_log+small_noise, y= y_val+noise, s=15, c="green", alpha=.7)
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