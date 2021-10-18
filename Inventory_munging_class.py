# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 09:03:05 2021

@author: chase
"""

import pandas as pd
import numpy as np
import datetime as dt

import Inventory_glob


# year = 2021
# month= 7
# day = 31

## MUST update file_input dates

path = r'C:\Users\chase\OneDrive\Desktop\Balance Sheet\Inventory\Ekos Inventory Analysis\Ekos Inv Downloads\[0-9]*.[0-9]*'


class InentoryMunging:
    def __init__(self):
        

    def bring_in(file): 
        """
        Bring in file
        
        Arg: str 
            file path
        
        returns: df
        
        """
        
        x = file
        y = x.replace('\\','/')
        
        return pd.read_excel(y)


    def location_col(df): 
        """
        Cleans the location column for downloaded document
        
        Arg: df
            file read in 
            
        Returns df
            document with new 'Location' column added
            
        """
        reg = 'Site : (.*)'
        df["Location"] = df['Inventory - As Of Date - Grouped by Item Class'].str.extract(reg).astype(str)
        df['Location'] = df["Location"].replace('nan', np.NaN, regex=False)
        df['Location'].ffill(inplace=True)
        
        return df

    def rename_cols(df): 
        """
        Renames all columns for this doc
        
        """
        
        cols = ['Item', 'Location2', 'Lot', 'Quantity', 'Unit of Measure', 'Average Cost', 'Total Value', 'Default Sale Price', 'Gallons', 'Liters', 'Case Eq.', 'Site']
        df.columns = cols
        
        return df

    def item_class_col(df): 
        """
        Cleans the 'Item Class' column for downloaded document
        
        Arg: df
            file read in 
            
        Returns df
            document with new 'Item Class' column added
            
        """
        
        reg2 = 'Item Class : (.*)'
        df["Item Class"] = df['Item'].str.extract(reg2).astype(str)
        df['Item Class'].replace('nan',np.nan, inplace=True)
        df['Item Class'].ffill(inplace=True)
        
        return df

    def drop_inv_rows(df):
        """
        Drops extra rows both head and tail of Inventory Doc
        
        Arg: df
        
        Returns: df
        
        """
        
        x = np.where(df['Item']=='Item')[0][0] + 1
        df = df[x:df.shape[0] + 1]
        df.reset_index(inplace=True, drop=True)

        return df

    def drop_inv_cols(df):
        """
        Cleans rows based on specific issues with this Inventory Doc
        
        Arg, Returns: df, df
        
        """
        df = df[~df['Lot'].str.contains("Lot", na=False)]
        df = df[~df['Gallons'].str.contains("SUM", na=False)]
        df = df[~df['Item'].str.contains("Class :", na=False)]
        df = df[~df['Item'].str.contains("Site :", na=False)]
        
        return df

    def inv_other_clean(df): 
        """
        Create datetime col and converts specific columns to floats
        
        Arg, Return: df, df
        
        """
        df['Inv Date'] = dt.datetime(year, month, day)
        cols_float = ['Quantity','Average Cost', 'Total Value', 'Gallons', 'Liters', 'Case Eq.'] 
        df[cols_float] = df[cols_float].astype('float')

        return df

    def inv_clean_out(df): 
        """
        Send cleaned/tidy data Inventory doc to 'Clean' folder 
        
        Arg: cleaned df using above functions
        
        Returns: finalized inventory list df
        
        """
        if month not in [10, 11, 12]:
            df.to_csv(f'C:/Users/chase/OneDrive/Desktop/Balance Sheet/Inventory/Ekos Inventory Analysis/Test/{year}.{month} Clean Inv_test.csv', index=False)
        else: 
            df.to_csv(f'C:/Users/chase/OneDrive/Desktop/Balance Sheet/Inventory/Ekos Inventory Analysis/Test/{year}.{month} Clean Inv_test.csv', index=False)

if __name__ == '__main__':
    
    files = Inventory_glob.get_files(path)
    
    for i in files:
        x = Inventory_glob.file_dates(files)
        year = x[0]
        month = x[1]
        day = x[2]
    
        df = bring_in(i)
        df = location_col(df)
        df = rename_cols(df)
        df = item_class_col(df)
        df = drop_inv_rows(df)
        df = drop_inv_cols(df)
        df = inv_other_clean(df)
        
        inv_clean_out(df)