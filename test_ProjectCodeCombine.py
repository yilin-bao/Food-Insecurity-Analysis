import ProjectCodeCombine as pcc

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

from unittest.mock import patch
import pytest

# Import Data
data_0911 = pd.read_excel(r'data/MMG2011_2009Data_ToShare.xlsx',sheet_name='2009 County',header = 0, dtype={"FIPS": str})
data_0911 = data_0911[0:3137]

snap = pd.read_excel(r'data/ACSST5Y2020.S2201-2022-05-24T041743.xlsx',sheet_name='Data',header = 0, dtype={"FIPS": str})
past_t = pd.read_csv('data/past_trend.csv')

data_race = pd.read_csv('data/2022 food insecurity vs race .csv')

def test_draw_FIrate():
    t = pcc.draw_FIrate()
    assert isinstance(t, pd.DataFrame)
    assert t.shape == (28282, 3)
    assert list(t) == ['FIPS', 'Rate of Food Insecurity', 'year']

def test_visualization_food_insecurity_map():
    assert isinstance(pcc.visualization_food_insecurity_map(pcc.draw_FIrate()), go.Figure)

def test_visualization_food_cost_map():
    assert isinstance(pcc.visualization_food_cost_map(data_0911), go.Figure)

def test_visualization_food_insecurity_plot():
    assert isinstance(pcc.visualization_food_insecurity_plot(past_t), go.Figure)

@patch("matplotlib.pyplot.show")
def test_visualization_food_insecurity_race(mock_show):
    pcc.visualization_food_insecurity_race(data_race)

def test_visualization_household():
    assert isinstance(pcc.visualization_household(snap), go.Figure)

def test_prepare_data():
    t = pcc.prepare_data()
    assert isinstance(t, pd.DataFrame)
    assert t.shape == (58, 7)
    assert list(t) == ['FIPS',
                     'CountyName',
                     'FI',
                     'FI_Density',
                     'Child_FI',
                     'Budget_Shortfall',
                     'FI_Change']

def test_rank_county():
    t = pcc.rank_county(pcc.prepare_data())
    assert isinstance(t, pd.DataFrame)
    assert t.shape == (58, 13)
    assert list(t) == ['FIPS',
                     'CountyName',
                     'FI',
                     'FI_Density',
                     'Child_FI',
                     'Budget_Shortfall',
                     'FI_Change',
                     'Rank_FI',
                     'Rank_FI_Density',
                     'Rank_Child_FI',
                     'Rank_Budget_Shortfall',
                     'Rank_FI_Change',
                     'FI_Ranking_Scores']

def test_result_visual():
    data = pcc.prepare_data()
    t = pcc.rank_county(data)
    assert isinstance(pcc.result_visual(t), go.Figure)