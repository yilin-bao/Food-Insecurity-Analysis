# Filename: county_ranking_model.py
# Author: Haoyu Wang, Jiaxuan Zhang
# Date: 05/27/2022
#
# Description:
#   This file will implement a model to capture county food insecurity ranking
# in California.It takes 5 factors into account: overall food insecurity(fi) rate,
# density of food insecure people, child fi rate, budget shortfall and fi changes
# in recent 2 years. The result will be visualized by a choropleth map where a
# dark color corresponds to a severe degree of food insecurity.
#
# Functions:
# prepare_data(): prepare the food insecurity data
# rank_county(): rank the county food insecurity degree
# result_visual(): visualize the result

import pandas as pd
import json
import plotly.express as px
from scipy.stats import rankdata
from urllib.request import urlopen

def prepare_data():
    '''
    This function will prepare the data in the following 5 categories:
    1. FI: overall food insecurity(fi) rate
    2. FI_Density: density of food insecure people
    3. Child_FI: child fi rate
    4. Budget: budget shortfall
    5. FI_Change: fi changes in recent 2 years

    :return: county FIPS, name and data above
    :rtype: pd.DataFrame
    '''

    # Read data from csv
    df = pd.read_csv('data/2019_fi_data.csv')
    df_2018 = pd.read_csv('data/2018_fi_data.csv')
    df_land_area = pd.read_csv('data/CA_land_area.csv',header=None)

    # Add 2018 fi data to main df
    df['2018 Food Insecurity Rate'] = df_2018['2018 Food Insecurity Rate']

    # Convert county names
    df['CountyName'] = df.loc[:,'County, State'].apply(lambda i: i.split(' County')[0])
    df.drop(['County, State'],axis=1,inplace=True)

    # Get land area data
    df_land_area['LandAreaInSqMi'] = df_land_area.loc[:,1].apply(lambda i: float(i.split()[0].replace(',','')))
    df_land_area['CountyName'] = df_land_area.loc[:,2].apply(lambda i: i.split(',')[0])
    df_land_area.drop([0,1,2],axis=1,inplace=True)

    # Add land area data to df
    df_land_area = df_land_area.sort_values(by='CountyName').reset_index()
    assert(list(df_land_area['CountyName']) == list(df['CountyName']))
    df['LandAreaInSqMi'] = df_land_area['LandAreaInSqMi']
    df.head()

    # Compute FI_Density
    df['FI_Density'] = df['# of Food Insecure Persons in 2019'] / df['LandAreaInSqMi']
    df.drop(['# of Food Insecure Persons in 2019','LandAreaInSqMi'],axis=1,inplace=True)

    # Compute FI_Change
    df['FI_Change'] = df['2019 Food Insecurity Rate'] - df['2018 Food Insecurity Rate']
    df.drop(['2018 Food Insecurity Rate'],axis=1,inplace=True)

    # Rename and order columns
    df = df.rename(columns={'2019 Food Insecurity Rate':'FI',
                       '2019 Child food insecurity rate':'Child_FI',
                       '2019 Weighted Annual Food Budget Shortfall':'Budget_Shortfall'})
    df = df[['FIPS','CountyName','FI','FI_Density','Child_FI','Budget_Shortfall','FI_Change']]

    return df

def rank_county(df):
    '''
    This function will rank the counties' food insecurity degree based on the 5 factors.
    A higher ranking score indicates the county has more severe food insecurity issues.
    :param df: dataframe returned from prepared_data :type: pd.DataFrame
    :return: prepared data with ranking data
    :rtype: pd.DataFrame
    '''

    # Give a ranking for each factor
    df['Rank_FI'] = rankdata(df['FI'])
    df['Rank_FI_Density'] = rankdata(df['FI_Density'])
    df['Rank_Child_FI'] = rankdata(df['Child_FI'])
    df['Rank_Budget_Shortfall'] = rankdata(df['Budget_Shortfall'])
    df['Rank_FI_Change'] = rankdata(df['FI_Change'])

    # Compute a overall ranking
    df['FI_Ranking_Scores'] = (df['Rank_FI']+df['Rank_FI_Density']+df['Rank_Child_FI']\
                         +df['Rank_Budget_Shortfall']+df['Rank_FI_Change'])/5

    return df

def result_visual(df):
    '''
    This function will visualize the result, a choropleth map, using the ranking data.
    :param df: dataframe returned from rank_county
    :return: none
    '''

    # Prepare FIPS and ranking data for plot
    df_plot = df[['FIPS','FI_Ranking_Scores']].copy()
    df_plot['FIPS'] = df_plot['FIPS'].apply(lambda i:'0'+str(i))
    min_score = min(list(df_plot['FI_Ranking_Scores']))
    df_plot['Food Insecurity Degree'] = df_plot['FI_Ranking_Scores'].apply(lambda i: i - min_score)
    max_score = max(list(df_plot['Food Insecurity Degree']))

    # Get json data
    url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
    with urlopen(url) as response:
        counties = json.load(response)

    # Plot color
    colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                  "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                  "#08519c","#0b4083","#08306b"]

    # Plot the graph
    fig = px.choropleth(df_plot, geojson=counties, locations='FIPS', color='Food Insecurity Degree',
                               color_continuous_scale=colorscale,
                               range_color=(0,max_score),
                               scope="usa"
                              )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()


## Visualize the result
#df = prepare_data()
#df = rank_county(df)
#result_visual(df)
