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

# Import data
df = pd.read_csv("data/canada.csv")


# Dropdown options
# Medal dropdwon
medal_list = "Gold Silver Bronze Total".split()
medal_options_dropdown = [{'label': medal, 'value': medal} for medal in medal_list]

# Attribute dropdown
attr_list = ['Name', 'Sport', 'Games', 'Season', 'City', 'Event', 'Sex', 'Age']
attribute_options_dropdown = [
    {'label':attribute, 'value': attribute} 
    for attribute in attr_list
]

# Set initial settings for figure1, time-figure
# Data
df_medal = af.count_medals_n(df, "Year")
# Slider options 
slider_marks = {
    str(year): str(year) for year in range(
        df["Year"].min(), df["Year"].max(), 2
    )
}

# Initiate dashboard
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
        min = df_medal[df_medal.columns[0]].min(), 
        max = df_medal[df_medal.columns[0]].max(), 
        step = 2,
        dots=True, 
        value=[
            df_medal[df_medal.columns[0]].min(), 
            df_medal[df_medal.columns[0]].max()
        ],
        marks = slider_marks
    ),

    html.H1("Top 10 - statistics for Canada"),
    html.H2('Choose statistic'),
    dcc.Dropdown(
        id = 'attribute-dropdown',
        className = '',
        value = "Sport",
        options = attribute_options_dropdown
    ),

    dcc.Graph(
        id='top10-graph',
        className=''
    ),
    # TODO figure with top ten best whatever!

    # TODO textbox with number of medals shown
    #    dbc.Col([
    #        dbc.Card([
    #            html.H2("Highest value", className='h5 mt-3 mx-3'),
    #            html.P(id = "highest-value", className='mx-3 h1 text-success')
    #        ], className='mt-5 w-50'),
    #        dbc.Card([
    #            html.H2("Lowest value", className='h5 mt-3 mx-3'),
    #            html.P(id = "lowest-value", className='mx-3 h1 text-danger'),
    #            ], className='w-50')


    #html.H2("International statistics")
    # TODO figures with international, Q2 results - Yuna does this
])

@app.callback(
    Output("medals-graph", "figure"),
    Input("medal-picker-dropdown", "value"),
    Input("time-slider", "value")
)
def update_graph(medal,time_index):
    """
    time_index is a list of two points choosen by user
    the left point refers to time_index[0]
    the right point refers to time_index[1]
    choose accordingly a subset of dataframe

    chosen_attribute is which column to split the medals into

    medal is type of medal, total, gold, silver, bronze

    This is inspired by "Create Dashboard in Plotly Dash with dependent drop down list (chained callbacks) and range slider":
    https://www.youtube.com/watch?v=TsYwhX0hEA8&t=244s
    """

    # Save number of medals per year
    df_medal = af.count_medals_n(df, "Year", "Season")

    # Set time range
    dff = df_medal[
        (df_medal[df_medal.columns[0]] >= time_index[0]) & 
        (df_medal[df_medal.columns[0]] <= time_index[1])
    ]
    
    # Update figure
    fig = px.bar(
        dff, x="Year", y=medal, color="Season",
        title=f"The number of {medal}s from {time_index[0]} to {time_index[1]}",
        labels={"value":"Number medals", "variable":"Medal"}
    )

    for data in fig.data:
        data["width"]= 0.5
    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    return fig

# Figure showing top10-statistics for Canada
@app.callback(
    Output("top10-graph", "figure"),
    Input("attribute-dropdown", "value"),
)
def update_graph(chosen_attribute):
    # Update df_medal after what is chosen
    df_top = af.count_medals_n(df, chosen_attribute)

    # Sort by attribute and extract top 10
    df_top = df_top.sort_values("Total", ascending=False)
    df_top = df_top.head(10)

    # Update figure
    fig = px.bar(
        df_top, x=chosen_attribute, y=medal_list,
        title=f"Canada, top 10 {chosen_attribute}",
        labels={"value":"Number medals", "variable":"Medal"}
    )
    fig.update_layout(barmode='group')

    return fig


if __name__ == '__main__':
    app.run_server(debug= True)
