import pandas as pd
import numpy as np
from dash import dcc, html
import dash
from load_data import ShowMeData
from dash.dependencies import Output, Input
import plotly_express as px
import plotly.graph_objects as go
from time_filtering import filter_time

# 1. Import data
df = pd.read_csv("data/canada.csv")
df_canada = pd.DataFrame(df.groupby(["Year", "Medal"]).count()["ID"]).reset_index()

# use df.pivot() for long-to-wide
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html#pandas.DataFrame.pivot
df_medal = df_canada.pivot(index="Year", columns="Medal", values="ID")
df_medal.fillna(0, inplace=True)
df_medal.reset_index(drop=False, inplace=True )
df_medal["Total"] = df_medal["Bronze"] + df_medal["Gold"] + df_medal["Silver"]
df_medal= df_medal.astype("int32")
df_medal['Year']= pd.to_datetime(df_medal['Year'], format='%Y').dt.year
# pd.to_datetime() generates Year-01-01 00:00:00
# add .dt.year to show only Year: https://stackoverflow.com/questions/51792903/use-only-year-for-datetime-index-pandas-dataframe
df_medal.head(10)

# Initiate dashboard

medal_options_dropdown = [{'label': medal, 'value': medal}
                          for medal in "Bronze Gold Silver Total".split()]
slider_marks = {str(year): str(year) for year in range(1896, 2017, 2)}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Canada in 120 years of Olympic history: athletes and results'),
    html.H2('Choose a medal:'),
    dcc.Dropdown(id='medal-picker-dropdown', className='',
                 value="Total",
                 options=medal_options_dropdown),
    dcc.Graph(id='medals-graph', className=''),
    dcc.RangeSlider(id='time-slider', className='',
                 min= 1896, max=2016, step=2,
                 dots=True, value=[1896, 2020],
                 marks = slider_marks),
    
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
    
    dff = df_medal[(df_medal["Year"]>=time_index[0]) & (df_medal["Year"]<=time_index[1])]
    fig = px.bar(dff, x="Year", y=medal, title=f"The number of {medal}s from {time_index[0]} to {time_index[1]}")

    for data in fig.data:
        data["width"]= 0.5
    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    
    return fig

if __name__ == '__main__':
    app.run_server(debug= True)