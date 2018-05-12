#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: airos

Does a quick check of SQL databases and tables.
Compares data by looking at each column's standard deviation, range, and inter-quartile range (if columns include floats)
Can also compare data depending on dependent variables.
Input required.

requires 'checkSQL_db.py' and 'checkSQL_UserFun.py' to be in same working directory
"""

from checkSQL_db_edit import Find_SQL_DB, Explore_SQL, Explore_Data, User_Input
from checkSQL_UserFun import show_options, getDataCont_Name, stop_OR_go, no_items
    
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
