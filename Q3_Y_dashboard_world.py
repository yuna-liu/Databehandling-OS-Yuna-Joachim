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
import sub_df as af2

# Import data
athlete_regions = pd.read_csv("data/athlete_regions.csv")
noc_iso = pd.read_csv("data/noc_iso.csv")

# Radio options
medal_options = [
    {'label': medal, 'value': medal}
    for medal in "Gold Silver Bronze Total".split()
]


# Dropdown options
# Attribute dropdown
attr_list = ['Sex', 'Age', 'Year', 'Season', 'City', 'Sport', 'Event']
attribute_options_dropdown = [
    {'label':attribute, 'value': attribute} 
    for attribute in attr_list
]

# Set initial settings
# Data
df = af2.count_medals(athlete_regions, "NOC", "Year")
df = df.reset_index()
df_iso = df.merge(noc_iso, on="NOC", how="left")
df_iso = df_iso.sort_values(by=["Year", "NOC"])

# Slider options 
slider_marks = {
    str(year): str(year) for year in range(
        df["Year"].min(), df["Year"].max(), 2
    )
}

# Initiate dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Global countries in 120 years of Olympic history: athletes and results'),

    html.P('Choose a attribute:'),    
    dcc.Dropdown(
        id='attribute-dropdown', 
        className='',
        value="Sex",
        options=attribute_options_dropdown
    ),
    html.P(id="total-medal"),
    html.P(id="gold-medal"),
    html.P(id="silver-medal"),
    html.P(id="bronze-medal"),
    dcc.RadioItems(id="medal-radio", className='',
                   options= medal_options,
                   value="Total"
                   ),
    
    dcc.Graph(
        id='medals-graph', 
        className=''
    ),

    #dcc.RangeSlider(
        #id='time-slider', 
        #className='',
        #min = df_iso[df_iso.columns[1]].min(), 
        #max = df_iso[df_iso.columns[1]].max(), 
        #step = 2,
        #dots=True, 
        #value=[
            #df_iso[df_iso.columns[1]].min(), 
            #df_iso[df_iso.columns[1]].max()
        #],
        #marks = slider_marks
    #),
        # stores an intermediate value on clients browser for sharing between callbacks
    dcc.Store(id="filtered-df")
])


    # TODO add this dashboard to the main dashboard

@app.callback(
    Output("medals-graph", "figure"),
    Input("filtered-df", "data"),
    Input("attribute-dropdown", "value"),
    Input("medal-radio", "value"),
    #Input("time-slider", "value")
)
#def update_graph(json_df, chosen_attribute, medal, x_index):
def update_graph(json_df, chosen_attribute, medal):
    # time_index is a list of two points choosen by user
    # the left point refers to time_index[0]
    # the right point refers to time_index[1]
    # choose accordingly a subset of dataframe
    # This is inspired by "Create Dashboard in Plotly Dash with dependent drop down list (chained callbacks) and range slider":
    # https://www.youtube.com/watch?v=TsYwhX0hEA8&t=244s

    # Update df_medal after what is chosen
    #if chosen_attribute != "Year":
        #df_medal = af.count_medals_n(df, "Year", chosen_attribute)
    #else:
        #df_medal = af.count_medals_n(df, "Year")

    # Set time range
    #dff = df_iso[
        #(df_iso[df_iso.columns[1]] >= x_index[0]) & 
        #(df_iso[df_iso.columns[1]] <= x_index[1])
    #]
    
    # Update figure
    #fig = px.bar(
        #dff, x="Year", y=medal, color=chosen_attribute,
        #title=f"The number of {medal}s from {x_index[0]} to {x_index[1]}"
    #)

    #for data in fig.data:
        #data["width"]= 0.5

    fig = px.choropleth(df_iso, locations="ISO",
                        color=medal,
                        scope=None,
                        hover_name="Country",
                        animation_frame="Year",
                        title = f"Geographic map on {medal} medals in the 120 Olympics history", 
                        range_color=[0,df_iso[medal].quantile(0.8)],
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    
    fig["layout"].pop("updatemenus")

    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    return fig

if __name__ == '__main__':
    app.run_server(debug= True)
