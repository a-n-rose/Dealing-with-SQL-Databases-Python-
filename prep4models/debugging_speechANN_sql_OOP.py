#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script pulls data from sqlite3 database and applies ANN to 12 MFCC columns and a binary label column
saves model to "engerm_annmodel_13mfcc_(num epochs)epochs.json" with weights saved to "engerm_annweights_13mfcc_(num epochs)epochs.hd"

This particular model uses 100 batch_size and 10 epochs
"""

 
import pandas as pd
import sqlite3
from sqlite3 import Error
import numpy as np
import time

import logging


from checkSQL_db_edit import Find_SQL_DB, Explore_SQL, User_Input, Prep_Data_DL
from checkSQL_UserFun_edit import show_options, getDataCont_Name, stop_OR_go, no_items


logger = logging.getLogger(__name__)



if __name__ == '__main__':
    
    #Search cwd for .db files 
    dbs = Find_SQL_DB()
    if dbs.item_list:
        while dbs.stop == False:
            
            #Presents User with Databases to choose from
            show_options(dbs)
            db_input = User_Input()
            db_name = getDataCont_Name(db_input,dbs)
            currdb = Explore_SQL(db_name)
            
            #Finds tables in the chosen Database
            tables = currdb.tables2list()
            if tables:
                while currdb.stop == False:
                    
                    #Presents User with Tables to choose from
                    show_options(currdb)
                    table_input = User_Input()
                    table_name = getDataCont_Name(table_input,currdb)
                    
                    ######################################################
                    
                    row_start = currdb.get_rowstart(table_name)
                    row_limit = currdb.get_rowlimit(table_name)
                    #turn into df
                    df = currdb.table2dataframe(table_name,row_start,row_lim)
                    
                    #explore this dataframe:
                    model = input("Which kind of model is this data for? (i.e. ANN, randomforest, linear regression, etc.): ")
                    currdf = Prep_Data_DL(df,model)
                    
                    ####### Prep data? One-Hot-Encoding? 
                        
                        
                        #need to allow the user to pull data from different tables
                        #and possibly other databases... Maybe a task for
                        #another time... 
                        
                        #if they want to apply a model on data from multiple places
                    
                
                
                
                
                    ######################################################
                #If there is only 1 table in the database, exit while statement
                    if len(tables) == 1:
                            currdb.stop == True
                    else:
                        #Ask User if they would like to look at another table
                        yes_no = stop_OR_go(currdb.datacont_type)
                        if 'no' in yes_no:
                            currdb.stop = True
           #If no tables found in database, let User know
            else:
                no_items('tables','database')
            
            #If only 1 database, exit while statement (and program)
            if len(dbs.item_list) == 1:
                dbs.stop = True
            #Otherwise, ask User if they would like to look in another database
            else:
                yes_no = stop_OR_go(dbs.datacont_type)
                if 'no' in yes_no:
                    dbs.stop = True
    #If no .db files found, let User know
    else:
        no_items('databases','directory')
    #Close sqlite3 connection without committing: just to make sure no changes that might somehow be made get saved
    currdb.close_conn_NOsave()
