#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:01:48 2018

@author: airos

These classes help to quickly explore what SQL databases and tables are available
as well as what type of data is inside them

It allows to quickly check for unusual data (std, range, iqr)

"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import glob


class Find_SQL_DB:
    '''
    Collects all databases in the current working directory
    stores them as list and as readable list (i.e without brackets)
    '''
    def __init__(self):
        self.db_list = [db for db in glob.glob('*.db')]
        self.db_names = '%s' % ', '.join(self.db_list)
        

class Explore_SQL:
    '''
    Explores what tables are available in a database
    Turns table of interest into a pandas dataframe
    '''
    def __init__(self,db_name):
        self.database = db_name
        self.conn = sqlite3.connect(db_name)
        self.c = sqlite3.connect(db_name).cursor()
        self.tables = "Not yet defined. Run the method 'print_tables' or 'tables2list' to set this attribute"
        
    def print_tables(self):
        try:
            self.c.execute("SELECT * FROM sqlite_master WHERE type='table';")
            table_list = self.c.fetchall()
            tables = [table_list[table][1] for table in range(len(table_list))]
            self.tables = "%s" % ", ".join(tables)
            print(self.tables)
        except Error as e:
            print(e)
            
        return None
    
    def tables2list(self):
        try:
            self.c.execute("SELECT * FROM sqlite_master WHERE type='table';")
            table_list = self.c.fetchall()
            tables = [table_list[table][1] for table in range(len(table_list))]
            self.tables = "%s" % ", ".join(tables)
            return(tables)
        except Error as e:
            print(e)
            
        return None
    
    def table2dataframe(self,table,row_start = None,row_lim=None):
        try: 
            if row_start and row_lim:
                first_row = str(row_start)
                limit = str(row_lim)
                self.c.execute("SELECT * FROM "+table+" LIMIT " + first_row +", " + limit)
            elif row_start:
                limit = str(row_start)
                self.c.execute("SELECT * FROM "+table+" LIMIT " + limit)
            else:
                self.c.execute("SELECT * FROM "+table)
            data = self.c.fetchall()
            return(pd.DataFrame(data))
        except Error as e:
            print(e)
        
        return None
    
    def close_conn_NOsave(self):
        self.conn.close()
        
    def close_conn_commit(self):
        self.conn.commit()
        self.conn.close()
    
class Explore_Data:
    '''
    Explores whether or not the last column (assumed to be dependent variable) contains categorical or continuous data
    Explores the standard deviation, range, and inter-quartile range of columns with type 'float' data 
    '''
    def __init__(self,df):
        self.dataframe = df
        self.columns = df.columns.get_values()
        self.num_rows = len(df)
        self.depvar = None
        self.depvar_type = None
        self.depvar_numunique = None
        self.spec_depvar = None
        
    def calc_std(self):
        if self.spec_depvar: 
            df = self.dataframe[self.dataframe[self.columns[-1]]==self.spec_depvar]
        else:
            df = self.dataframe
        data_std = [(self.columns[col],np.std(df[col])) for col in range(len(self.columns)) if isinstance(df[col].iloc[0],float)]
        return(data_std)
        
    def calc_range(self):
        if self.spec_depvar: 
            df = self.dataframe[self.dataframe[self.columns[-1]]==self.spec_depvar]
        else:
            df = self.dataframe
        data_range = [(self.columns[col],(max(df[col])-min(df[col]))) for col in range(len(self.columns)) if isinstance(df[col].iloc[0],float)]
        return(data_range)
    
    def calc_iqr(self):
        if self.spec_depvar: 
            df = self.dataframe[self.dataframe[self.columns[-1]]==self.spec_depvar]
        else:
            df = self.dataframe
        data_iqr = [(self.columns[col],np.subtract(*np.percentile(df[col],[75,25]))) for col in range(len(self.columns)) if isinstance(df[col].iloc[0],float)]
        return(data_iqr)
        
    def explore_depvar(self):
        last_col = self.columns[-1]
        self.depvar_type = type(self.dataframe[last_col][0])
        self.depvar = set(self.dataframe[last_col])
        self.depvar_numunique = len(self.depvar)
        return None
    
    def print_profile(self,table_name,dep_var = None):
        try:
            self.spec_depvar = dep_var
            print()
            print('#'*80,'\n')
            print("SQL table --",table_name,"-- profile: \n")
            print("Columns: \n", self.columns)
            self.explore_depvar()
            print()
            print("Dependent variable (i.e. column {}) type: \n".format(self.columns[-1]), self.depvar_type,"\n")
            print("Number of dependent variables: \n", self.depvar_numunique,"\n")
            print("Dependent variable(s): \n",self.depvar,"\n")
            if dep_var:
                print("Dependent variable of interest: ",self.spec_depvar,"\n")
            print("Standard deviation of applicable columns: \n",self.calc_std(),"\n")
            print("Range of applicable columns: \n", self.calc_range(),"\n")
            print("Inter-quartile Range of applicable columns: \n",self.calc_iqr(),"\n")
            print('#'*80)
            print()
        except Exception as e:
            print(e)
            
        return None
    
    
class User_Input:
    def __init__(self,text):
        self.text = text
        
    def str2index(self,items_list):
        try:
            ind = int(self.text)-1
            if ind >= 0:
                requested_item = items_list[ind]
                return(requested_item,True)
            else:
                print("\nPlease enter an integer between 1 and "+(str(len(items_list)))+'\n')
        except ValueError as ve:
            print(Error_Msg().msg)
            print(ve)
            print("\nValue must be an integer\n".upper())
            print(Error_Msg().att)
        except IndexError as ie:
            print(Error_Msg().msg)
            print(ie)
            if len(items_list) > 1:
                err_msg = "\nPlease enter an integer between 1 and "+(str(len(items_list)))+'\n'
            else:
                err_msg = "\nPlease enter '1' if you would like to continue\n"
            print(err_msg.upper())
            print(Error_Msg().att)
        return None, False
        

class Error_Msg:
    def __init__(self):
        self.msg = '\n\n\n'+('!*'*10)+' ERROR! '+'!*'*10+'\n'
        self.att = '!*'*24
