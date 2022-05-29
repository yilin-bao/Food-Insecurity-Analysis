# Filename: extract_data.py
# Author: Haoyu Wang
# Description: This file extracts data from 'Map the Meal Gap' dataset for
# CA county food insecurity ranking model. The output files are
# 2018_fi_data.csv and 2019_fi_data.csv.

import pandas as pd

def extract_mmp_data(year=2019, state='CA',output=True):
    '''
    This function extract the data from the 'Map the Meal Gap' dataset
    for implementing CA county food insecurity ranking model. If output is true,
    it will save the extracted data as year_fi_data.csv in the current directory.
    Else, it will return the dataframe.
    To call this function, make sure the original MMG dataset is in the current
    directory.
    :param year: data of the year   :type: int
    :param state: state name        :type: str
    :param output: flag for output  :type: bool
    :return: data in pd.DataFrame if output is true
    '''

    # Check the input parameters
    assert(isinstance(year,int))
    assert(2018<=year<=2019)
    assert(isinstance(state,str))

    # Read data from MMG data
    file_name = 'MMG'+str(year+2)+'_'+str(year)+'Data_ToShare.xlsx'
    xls = pd.ExcelFile(file_name)
    df = pd.read_excel(xls, str(year)+' County')
    if year==2018:
        df.columns = df.iloc[0]

    # Select the state
    df_state = df.loc[df.State==state,:]

    # Select the features
    sel_cols = ['FIPS', 'County, State', str(year)+' Food Insecurity Rate',
            '# of Food Insecure Persons in '+str(year),
            str(year)+' Child food insecurity rate',
            str(year)+' Weighted Annual Food Budget Shortfall']

    df = df_state.loc[:,sel_cols]

    if not output:
        return df

    else:
        # Save as csv
        df.to_csv(str(year)+'_fi_data.csv',index=False)
        return None


# Extract the data and save the output
extract_mmp_data(year=2019,state='CA',output=True)
extract_mmp_data(year=2018,state='CA',output=True)
