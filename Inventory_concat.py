# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 09:50:26 2021

@author: chase
"""

import glob
import pandas as pd


### Load files from directory file

df_files = glob.glob('C:/Users/chase/OneDrive/Desktop/Balance Sheet/Inventory/Ekos Inventory Analysis/Clean/20[1-2][0-9]*.csv', recursive=False)



                     
print(df_files)


def combine_files():
    results = pd.DataFrame([])
    for filename in df_files: 
        print(filename)
        namedf = pd.read_csv(filename, header=0)
        results = results.append(namedf)
        
    results.reset_index(inplace=True, drop=True)
    results.to_csv(r'C:\Users\chase\My Tableau Repository\Datasources\Inventory\Inv_Balance_monthly.csv', index=False)
    
if __name__ == '__main__':
    
    combine_files()


