import pandas as pd
from dash import dcc, html
import dash
from load_data import ShowMeData
from dash.dependencies import Output, Input
import plotly_express as px
from time_filtering import filter_time

list_canada = []
canada = pd.read_csv("data/canada.csv", index_col = 0, parse_dates = True)
canada.reset_index(drop=True)
list_canada.append(canada)
list_canada
