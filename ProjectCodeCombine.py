import pandas as pd 
import matplotlib.pyplot as plt 
import imageio, os
import numpy as np
from urllib.request import urlopen
import json
import math
import plotly
import plotly.figure_factory as ff
import plotly.express as px
import plotly.offline as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot
from plotly import tools
from plotly.subplots import make_subplots
from scipy.stats import rankdata
from urllib.request import urlopen

# Import Data
data_0911 = pd.read_excel(r'data/MMG2011_2009Data_ToShare.xlsx',sheet_name='2009 County',header = 0, dtype={"FIPS": str})
data_0911 = data_0911[0:3137]

snap = pd.read_excel(r'data/ACSST5Y2020.S2201-2022-05-24T041743.xlsx',sheet_name='Data',header = 0, dtype={"FIPS": str})
past_t = pd.read_csv('data/past_trend.csv')

data_race = pd.read_csv('data/2022 food insecurity vs race .csv')

# Models
def draw_FIrate():
    df = pd.DataFrame()
    for year in range(2010, 2019):
        year2 = str(year+2)
        if year == 2018:
            data = pd.read_excel(
                'data/MMG{0}_{1}Data_ToShare.xlsx'.format(year2,year),
                sheet_name='{} County'.format(year),
                header = 1, 
                dtype={"FIPS": str})
        else:
            
            data = pd.read_excel(
                'data/MMG{0}_{1}Data_ToShare.xlsx'.format(year2,year),
                sheet_name='{} County'.format(year),
                header = 0, 
                dtype={"FIPS": str})
        data = data[["FIPS", '{} Food Insecurity Rate'.format(year)]]
        data['FIPS'] = data['FIPS'].apply(lambda x:str(x).rjust(5,'0') )
        data = data.rename(columns={'FIPS': "FIPS", '{} Food Insecurity Rate'.format(year): "Rate of Food Insecurity"})
        data['year'] = year
        
        if df.empty:
            df = data
        else:
            df = df.append(data)
    return df

def visualization_food_insecurity_map(df):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                "#08519c","#0b4083","#08306b"]
    fig = px.choropleth(df, 
                        geojson=counties,
                        locations='FIPS',
                        color= "Rate of Food Insecurity",
                        color_continuous_scale=colorscale,
                        animation_frame='year',
                        range_color=(0, 0.4),
                        scope="usa",
                        labels={'fi':"Rate of Food Insecurity"}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def visualization_food_cost_map(data):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    map_test = data_0911[['FIPS','2009 Cost Per Meal']]
    colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                  "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                  "#08519c","#0b4083","#08306b"]
    endpts = list(np.linspace(1, 12, len(colorscale) - 1))
    fig2 = px.choropleth(map_test,geojson=counties, locations='FIPS', color='2009 Cost Per Meal',
                               color_continuous_scale="Oranges",
                               range_color=(min(data_0911['2009 Cost Per Meal']), max(data_0911['2009 Cost Per Meal'])),
                               scope="usa",
                               labels={'fi':'2009 Cost Per Meal'}
                              )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig2

def visualization_food_insecurity_plot(data):
    data = past_t
    data['mean'] = list(data.mean(axis=1, numeric_only=True))
    low_fi = data[data['mean']<0.12]
    low_fi['mean'] = low_fi['mean'] *100
    low_fi = low_fi.round(1)
    mid_fi = data[((data['mean']>=0.12) & (data['mean']<0.14))]
    mid_fi['mean'] = mid_fi['mean'] *100
    mid_fi = mid_fi.round(1)
    high_fi = data[(data['mean']>=0.14)]
    high_fi['mean'] = high_fi['mean'] *100
    high_fi = high_fi.round(1)
    x = [i for i in range(100)]
    df_1 = low_fi
    df_2 = mid_fi
    df_3 = high_fi

    labels = ["low_FI States", "Mid_FI States","High_FI States"]

    fig = tools.make_subplots(rows=1, cols=2)

    trace1 = go.Bar(x=df_1.State, y=df_1["mean"], showlegend=True)
    fig.append_trace(trace1, 1, 1)

    trace2 = go.Bar(x=df_2.State, y=df_2["mean"], showlegend=True)
    fig.append_trace(trace2, 1, 1)

    trace3 = go.Bar(x=df_3.State, y=df_3["mean"], showlegend=True)
    fig.append_trace(trace3, 1, 1)
    
    buttons = []
    for i, label in enumerate(labels):
        visibility = [i==j for j in range(len(labels))]
        button = dict(label =  label, method = 'update', args = [{'visible': visibility}, {'title': label}])
        buttons.append(button)
    updatemenus = list([dict(active=-1, x=-0.15, buttons=buttons)])

    fig['layout']['title'] = 'Average Food Insecurity Rate Over 2009-2019 for Different States'
    fig['layout']['showlegend'] = False
    fig['layout']['updatemenus'] = updatemenus
    return fig

def visualization_food_insecurity_race(data):
    plt.figure(figsize=(15,8))
    states= ["CA",'TX','FL','NY','PA','IL','OH','GA','NC','MI']      
    California = {}
    asian = [i for i in data['Asian_s'] if math.isnan(i) == False]
    white = [i for i in data['white_s'] if math.isnan(i) == False]
    black = [i for i in data['black_s'] if math.isnan(i) == False]
    latino =[i for i in data['Hispanic_s'] if math.isnan(i) == False] 
    other = [i for i in data['other_s'] if math.isnan(i) == False]
    ind = np.arange(len(states)) 
    width = 0.15
    plt.bar(ind,asian,width,color='#c35b7e',label = 'Asian')
    plt.bar(ind+width,white,width,color='#910736',label = 'White')
    plt.bar(ind+width*2,black,width,color='#866ba8',label = 'Black')
    plt.bar(ind+width*3,latino,width,color='#f13710',label = 'Hispanic or Latino')
    plt.bar(ind+width*4,other,width,color='#f8c928',label = 'Other race')
    plt.xticks(ind, states)
    plt.legend(loc='upper right')
    plt.ylabel("Percent%")
    plt.xlabel("States")
    plt.title('Food Insecurity percent in each states with different races')
    plt.ylim(5, 50)
    plt.show()

def visualization_household(snap):
    labels = ["Household construction", "With elders or not","Number of workers", "Ethnicity"]

    fig = plotly.subplots.make_subplots(rows=1, cols=2)
    sizes = [snap.iloc[6, 3]] + list(snap.iloc[8:10, 3])
    for i in range(len(sizes)):
        sizes[i] = float(sizes[i].replace('%', ''))

    trace1 = go.Bar(y=sizes, x=[snap.iloc[6, 0]] + list(snap.iloc[8:10, 0]), showlegend=True)

    fig.append_trace(trace1, 1, 1)

    sizes = list(snap.iloc[3:5, 3])
    for i in range(len(sizes)):
        sizes[i] = float(sizes[i].replace('%', ''))
    trace2 = go.Bar(x=list(snap.iloc[3:5, 0]), y=sizes, showlegend=True)

    fig.append_trace(trace2, 1, 1)

    sizes = list(snap.iloc[43:46, 3])
    for i in range(len(sizes)):
        sizes[i] = float(sizes[i].replace('%', ''))
    trace3 = go.Bar(x=list(snap.iloc[43:46, 0]), y=sizes, showlegend=True)

    fig.append_trace(trace3, 1, 1)

    sizes = list(snap.iloc[30:38, 3])
    for i in range(len(sizes)):
        sizes[i] = float(sizes[i].replace('%', ''))
    trace4 = go.Bar(x=list(snap.iloc[30:38, 0]), y=sizes, showlegend=True)

    fig.append_trace(trace4, 1, 1)

    buttons = []
    for i, label in enumerate(labels):
        visibility = [i==j for j in range(len(labels))]
        button = dict(label =  label, method = 'update', args = [{'visible': visibility}, {'title': label}])
        buttons.append(button)

    updatemenus = list([dict(active=-1, x=-0.15, buttons=buttons)])

    fig['layout']['title'] = 'Snap Ratio by Household Types'
    fig['layout']['showlegend'] = False
    fig['layout']['updatemenus'] = updatemenus

    return fig

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
    return fig
    
# Process
visualization_food_insecurity_map(draw_FIrate())

visualization_food_cost_map(data_0911)

visualization_food_insecurity_plot(past_t)

visualization_food_insecurity_race(data_race)

visualization_household(snap)

result_visual(rank_county(prepare_data()))
