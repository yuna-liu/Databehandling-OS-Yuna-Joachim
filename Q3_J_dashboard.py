import pandas as pd
import numpy as np
from dash import dcc, html
import dash
from load_data import ShowMeData
from dash.dependencies import Output, Input
import plotly_express as px
import plotly.graph_objects as go
from time_filtering import filter_time

import analyze_functions as af

# 1. Import data
df = pd.read_csv("data/canada.csv")



# TODO: use medal counter function after slider options
# Dropdown options are to be the columns in df (except number of medals)
# Slider options are to be the the range of values in the column the user choses
# Dropdown menu to chose summer/winter/both

# The column name here should be chosen from the Dropdown menu
df_medal = af.count_medals_n(df, "Year")


# Initiate dashboard

# Dropdown options
medal_options_dropdown = [{'label': medal, 'value': medal}
                          for medal in "Gold Silver Bronze Total".split()]

# Slider options
slider_marks = {str(year): str(year) for year in range(1896, 2017, 2)}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Canada in 120 years of Olympic history: athletes and results'),
    html.H2('Choose a medal:'),
    
    dcc.Dropdown(
        id='medal-picker-dropdown', 
        className='',
        value="Total",
        options=medal_options_dropdown
    ),
    
    dcc.Graph(
        id='medals-graph', 
        className=''
    ),
    dcc.RangeSlider(
        id='time-slider', 
        className='',
        min= 1896, max=2016, step=2,
        dots=True, value=[1896, 2020],
        marks = slider_marks
    ),
])


@app.callback(Output("medals-graph", "figure"),
              Input("medal-picker-dropdown", "value"),
              Input("time-slider", "value")
              )
def update_graph(medal, time_index):
    # time_index is a list of two points choosen by user
    # the left point refers to time_index[0]
    # the right point refers to time_index[1]
    # choose accordingly a subset of dataframe
    # This is inspired by "Create Dashboard in Plotly Dash with dependent drop down list (chained callbacks) and range slider":
    # https://www.youtube.com/watch?v=TsYwhX0hEA8&t=244s
    
    dff = df_medal[(df_medal.index>=time_index[0]) & (df_medal.index<=time_index[1])]
    
    fig = px.bar(
        dff, x=dff.index, y=medal, 
        title=f"The number of {medal}s from {time_index[0]} to {time_index[1]}"
    )

    for data in fig.data:
        data["width"]= 0.5
    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    
    return fig

if __name__ == '__main__':
    app.run_server(debug= True)
