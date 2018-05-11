#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:29:05 2018

@author: airos

Does a quick check of SQL databases and tables.
Compares data by looking at each column's standard deviation, range, and inter-quartile range (if columns include floats)
Can also compare data depending on dependent variables.
Input required.

requires 'checkSQL_db.py' to be in same working directory
"""

from checkSQL_db_edit import Find_SQL_DB, Explore_SQL, Explore_Data, User_Input

def show_options(datacont_instance):
    data_cont = datacont_instance.datacont_type
    data_list = datacont_instance.item_list
    print("\nAvailable {}:".format(data_cont))
    for item in range(len(data_list)):
        print("{}) ".format(item+1), data_list[item])
    print("\nWhich {} would you like to explore?".format(data_cont))
    return None

def getDataCont_Name(input_instance,datacont_instance):
    ii = input_instance
    di = datacont_instance
    data_cont = di.datacont_type
    while ii.stop == False:
        ii.text = input('Please enter the number corresponding to the {}: '.format(data_cont))
        #checks the input and gets database name
        datacont_name, ii.stop = ii.str2index(di.item_list)
    return(datacont_name)
    
if __name__ == '__main__':
    
    #first collect database names in current working directory (i.e. '.db' files)
    dbs = Find_SQL_DB()
    #dbs_list = dbs.db_list
    if dbs.item_list:
        #exp_databases = True
        while dbs.stop == False:
            #database_entry = False
            
            #list databases with a number for user to choose which to work with
            show_options(dbs)
            db_input = User_Input()
            db_name = getDataCont_Name(db_input,dbs)
                
            #establishes connection with SQL database via sqlite3
            #then list tables for user to choose which to work with
            currdb = Explore_SQL(db_name)
            tables = currdb.tables2list()
            if tables:
                
                #list tables in database for user to choose from
                show_options(currdb)
                table_input = User_Input()
                table_name = getDataCont_Name(table_input,currdb)
                
                #converts table data to pandas df
                df = currdb.table2dataframe(table_name)
                #conduct calculations and "learn" about data in table
                currdf = Explore_Data(df)
                currdf.print_profile(table_name)
                if currdf.depvar_numunique > 1:
                    cont_explore = False
                    while cont_explore == False:
                        
                        #ask user if they would like to look at another variable
                        examfurth = input("\nWould you like to explore data from a particular dependent variable? (yes or no): ")
                        if 'no' in examfurth.lower():
                            pause_explore = True
                            
                            #check if the user wants to explore data in another database before leaving program
                            if len(dbs.item_list) > 1:
                                extra_db = False
                                while extra_db == False:
                                    another_db = input("\nWould you like to explore data from another database? (yes or no): ")
                                    if 'no' in another_db.lower():
                                        dbs.stop = True
                                        break
                                    elif 'yes' in another_db.lower():
                                        extra_db = True
                                    else:
                                        print("\nPlease enter 'yes' or 'no'\n")
                            break
                        elif 'yes' in examfurth.lower():
                            cont_explore = True
                            pause_explore = False
                        else: 
                            print("\nPlease enter 'yes' or 'no'\n")           
                    
                    #if user wants to explore the data in the dependent variables
                    #list of the dependent variables with corresponding numbers --> user chooses which variable
                    dv_list = list(currdf.depvar)
                    while pause_explore == False:
                        show_options(currdf)
                        dv_input = User_Input()
                        dv_name = getDataCont_Name(dv_input,currdf)
                        if dv_input.stop == True:
                            pause_explore = True
                        currdf.print_profile(table_name, dv_name)
                        again = False
                        while again == False and pause_explore == True:
                            
                            #See if the user wants to continue exploring with another dependent variable
                            expmore = input("\nWould you like to explore another dependent variable? (yes or no): ")
                            if 'no' in expmore.lower():
                                pause_explore = True
                                if len(dbs.item_list) > 1:
                                    extra_db = False
                                    while extra_db == False:
                                        another_db = input("\nWould you like to explore data from another database? (yes or no): ")
                                        
                                        #If user doesn't want to, check if they want to check out another database (if there's more than one)
                                        if 'no' in another_db.lower():
                                            dbs.stop = True
                                            break
                                        elif 'yes' in another_db.lower():
                                            extra_db = True
                                            currdb.close_conn_NOsave()
                                        else:
                                            print("\nPlease enter 'yes' or 'no'\n")
                                break
                            elif 'yes' in expmore.lower():
                                again = True
                                pause_explore = False
                            else:
                                print("\nPlease enter 'yes' or 'no'\n")
                
                #if only 1 dependent variable and multiple databases, check if the user wants to look at other databases
                if len(dbs.item_list) > 1:
                    extra_db = False
                    while extra_db == False and dbs.stop == False:
                        another_db = input("\nWould you like to explore data from another database? (yes or no): ")
                        if 'no' in another_db.lower():
                            dbs.stop = True
                            break
                        elif 'yes' in another_db.lower():
                            extra_db = True
                            currdb.close_conn_NOsave()
                        else:
                            print("\nPlease enter 'yes' or 'no'\n")
            
            else:
                print("\n!! No tables found in database\n")
    else:
        print("\n!! No databases found\n")
    currdb.close_conn_NOsave()
