import pandas as pd
import numpy as np
from dash import dcc, html
import dash
from load_data import ShowMeData
from dash.dependencies import Output, Input
import plotly_express as px
import plotly.graph_objects as go
from time_filtering import filter_time
import dash_bootstrap_components as dbc

import analyze_functions as af
import sub_df as af2

# Import data
athlete_regions = pd.read_csv("data/athlete_regions.csv")
noc_iso = pd.read_csv("data/noc_iso.csv")
noc_iso = noc_iso.iloc[:, 1:]

# Radio options
medal_options = [
    {'label': medal, 'value': medal}
    for medal in "Gold Silver Bronze Total".split()
]


# Dropdown options
# Attribute dropdown
sport_list = athlete_regions['Sport'].unique().tolist()
sport_list.append("All")
sport_list.sort()
sport_options_dropdown = [
    {'label':sport, 'value': sport} 
    for sport in sport_list
]

# Set initial settings
# Data for all sports
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

stylesheets = [dbc.themes.MATERIA]
# creates a Dash App
app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

server = app.server  # needed for Heroku to connect to

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            html.H1('Global countries in 120 years of Olympic history: athletes and results',
                    className='card-title text-dark mx-3')
        ])
    ], className="mt-4"),

    dbc.Row(className='mt-4', children=[
        dbc.Col(
            # responsivity
            html.P("Choose sport:"), xs="12", sm="12", md="6", lg="4", xl={"size": 1, "offset": 2},
            className="mt-1"
        ),
        dbc.Col(
            dcc.Dropdown(id='sport-dropdown', className='',
                         options=sport_options_dropdown,
                         value='All',
                         placeholder='All'), xs="12", sm="12", md="12", lg="4", xl="3"),

        dbc.Col([
            dbc.Card([
                dcc.RadioItems(id='medal-radio', className="m-1",
                                  options=medal_options,
                                  value='Total'
                               ),
            ])
        ], xs="8", sm="8", md="8", lg='3', xl="1"),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="medals-graph"),
            
        ], lg={"size": "6", "offset": 1}, xl={"size": "6", "offset": 1}),

        # dbc.Col([
        #     dbc.Row(
        #         dbc.Card([
        #             html.H2("Highest value", className="h5 mt-3 mx-3"),
        #             html.P(id="highest-value", className="text-success h1 mx-2")
        #         ]), className="mt-5 h-25"
        #     ),
        #     dbc.Row(
        #         dbc.Card([
        #             html.H2("Lowest value", className="h5 mt-3 mx-3"),
        #             html.P(id="lowest-value", className="text-danger h1 mx-2")
        #         ]),
        #         className="mt-5 h-25"
        #     ),
        # ], sm="5", md="3", lg="3", xl="2", className="mt-5 mx-5"),

        html.Footer([
            html.H3("120 years of Olympic games", className="h6"),
            html.P("Dashboard av Yuna och Joachim")],
            className="navbar fixed-bottom")

    ]),
    # stores an intermediate value on the clients browser for sharing between callbacks
    dcc.Store(id="filtered-df"),

], fluid=True)



@app.callback(Output("filtered-df", "data"), Input("sport-dropdown", "value"),
              )
def filter_df(sport):
    """Filters the dataframe and stores it intermediary for usage in callbacks
    Returns:
        a dataframe for chosen sport
    """
    # Data for all sports
    if sport=="All":
        dff = df_iso
    else:
        df_sport = athlete_regions[athlete_regions['Sport']==sport]
        df_sport = af2.count_medals(df_sport, "NOC", "Year")
        df_sport = df_sport.reset_index()
        dff = df_sport.merge(noc_iso, on="NOC", how="left")
        dff = dff.sort_values(by=["Year", "NOC"])

    return dff.to_json()

# when something changes in the input component, the code in function below will run and update the output component
# the components are connected through their id



@app.callback(
    Output("medals-graph", "figure"),
    Input("filtered-df", "data"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value"),
    #Input("time-slider", "value")
)
#def update_graph(json_df, chosen_sport, medal, x_index):
def update_graph(json_df, chosen_sport, medal):

    dff = pd.read_json(json_df)
    fig = px.choropleth(dff, locations="ISO",
                        color=medal,
                        scope=None,
                        hover_name="Country",
                        animation_frame="Year",
                        title = f"Geographic map on {chosen_sport} {medal} medals in the 120 Olympics history", 
                        range_color=[0,dff[medal].quantile(0.9)],
                        color_continuous_scale=px.colors.sequential.Plasma)
      
    fig["layout"].pop("updatemenus")
    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    return fig

if __name__ == '__main__':
    app.run_server(debug= True)
