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



# TODO: 
# Slider options are to be the the range of values in the column the user choses



# Dropdown options
# Medal dropdwon
medal_options_dropdown = [
    {'label': medal, 'value': medal}
    for medal in "Gold Silver Bronze Total".split()
]

# Attribute dropdown
attribute_options_dropdown = [
    {'label':attribute, 'value': attribute} 
    for attribute in df.columns[4:16]
]

# Set initial settings
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

    html.H2('Choose colour bar value'),
    dcc.Dropdown(
        id = 'attribute-dropdown',
        className = '',
        value = "Year",
        options = attribute_options_dropdown
    ),

    dcc.Graph(
        id='medals-graph', 
        className=''
    ),

    dcc.RangeSlider(
        id='x-slider', 
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
])

@app.callback(
    Output("medals-graph", "figure"),
    Input("medal-picker-dropdown", "value"),
    Input("attribute-dropdown", "value"),
    Input("x-slider", "value")
)
def update_graph(medal,chosen_attribute ,x_index):
    # time_index is a list of two points choosen by user
    # the left point refers to time_index[0]
    # the right point refers to time_index[1]
    # choose accordingly a subset of dataframe
    # This is inspired by "Create Dashboard in Plotly Dash with dependent drop down list (chained callbacks) and range slider":
    # https://www.youtube.com/watch?v=TsYwhX0hEA8&t=244s

    # Update df_medal after what is chosen
    if chosen_attribute != "Year":
        df_medal = af.count_medals_n(df, "Year", chosen_attribute)
    else:
        df_medal = af.count_medals_n(df, "Year")

    # Set time range
    dff = df_medal[
        (df_medal[df_medal.columns[0]] >= x_index[0]) & 
        (df_medal[df_medal.columns[0]] <= x_index[1])
    ]
    
    # Update figure
    fig = px.bar(
        dff, x="Year", y=medal, color=chosen_attribute,
        title=f"The number of {medal}s from {x_index[0]} to {x_index[1]}"
    )
    fig.update_layout(barmode="group")

    for data in fig.data:
        data["width"]= 0.5
    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    return fig

if __name__ == '__main__':
    app.run_server(debug= True)
