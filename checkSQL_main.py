#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
        datacont_name, ii.stop = ii.str2index(di.item_list)
    return(datacont_name)
    
def stop_OR_go(data_container):
    cont_input = User_Input()
    while cont_input.stop == False:
        cont_input.text = input("\nWould you like to explore data from additional {}? (yes or no): ".format(data_container))
        if 'yes' or 'no' in cont_input.text.lower():
            cont_input.stop = True
            return(cont_input.text)
        else:
            print("\nPlease enter 'yes' or 'no'\n")
    return None  

def no_items(data_container1, data_container2):
    print("\n!! No %s found in %s !!\n" % (data_container1,data_container2))
    return None
    
if __name__ == '__main__':
    dbs = Find_SQL_DB()
    if dbs.item_list:
        while dbs.stop == False:
            show_options(dbs)
            db_input = User_Input()
            db_name = getDataCont_Name(db_input,dbs)
            currdb = Explore_SQL(db_name)
            tables = currdb.tables2list()
            if tables:
                while currdb.stop == False:
                    show_options(currdb)
                    table_input = User_Input()
                    table_name = getDataCont_Name(table_input,currdb)
                    df = currdb.table2dataframe(table_name)
                    currdf = Explore_Data(df)
                    currdf.print_profile(table_name)
                    if currdf.depvar_numunique == 1:
                        currdf.stop = True
                    while currdf.stop == False:
                        yes_no = stop_OR_go(currdf.datacont_type)
                        if 'no' in yes_no:
                            currdf.stop = True
                        else:
                            show_options(currdf)
                            dv_input = User_Input()
                            dv_name = getDataCont_Name(dv_input,currdf)
                            if dv_input.stop == True:
                                currdf.print_profile(table_name, dv_name)        
                    if len(tables) == 1:
                            currdb.stop == True
                    else:
                        yes_no = stop_OR_go(currdb.datacont_type)
                        if 'no' in yes_no:
                            currdb.stop = True
            else:
                no_items('tables','database')
            if len(dbs.item_list) == 1:
                dbs.stop = True
            else:
                yes_no = stop_OR_go(dbs.datacont_type)
                if 'no' in yes_no:
                    dbs.stop = True
    else:
        no_items('databases','directory')
    currdb.close_conn_NOsave()
