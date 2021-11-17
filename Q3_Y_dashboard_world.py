import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly_express as px

import analyze_functions as af

# Import data
athlete_regions = pd.read_csv("data/athlete_regions.csv")
athlete_iso = pd.read_csv("data/athlete_iso.csv").iloc[:, 1:]
noc_iso = pd.read_csv("data/noc_iso.csv").iloc[:, 1:]

# Radio options
medal_list = "Gold Silver Bronze Total".split()
medal_options = [{'label': medal, 'value': medal} for medal in medal_list]


# Dropdown options
# Sport dropdown
sport_list = athlete_regions['Sport'].unique().tolist()
sport_list.append("All Sports")
sport_list.sort()
sport_options_dropdown = [
    {'label':sport, 'value': sport} 
    for sport in sport_list
]

# Region dropdown
athlete_regions = athlete_regions[athlete_regions['region'].notna()]
region_list = athlete_regions['region'].unique().tolist()
region_list.append("All regions")
region_list.sort()
region_options_dropdown = [
    {'label':country, 'value': country} 
    for country in region_list
]


# Attribute dropdown options
attr_dict = {
    'Sport':'Sport', 
    'Event':'Sport event', 
    'Games':'Year & Season',
    'Season':'Season', 
    'Name':'Athlete', 
    'Sex':'Athlete genders', 
    'Age':'Athlete ages',
    'City':'City'
}
attribute_options_dropdown = [
    {'label':name, 'value': attribute} 
    for attribute, name in attr_dict.items()
]


# Athletes dropdown options
gender_options = [
    {'label':'Both', 'value':'Both'},
    {'label':'Female', 'value':'F'},
    {'label':'Male', 'value':'M'}
]
athlete_dict = {
    'Sex':'Gender',
    'Age':'Age',
    'Height':'Height',
    'Weight':'Weight'
}
unit_dict = {
    'Sex':'Gender',
    'Age':'Age (years)',
    'Height':'Height (centimetres)',
    'Weight':'Weight (kilograms)'
}

athlete_options = [
    {'label':name, 'value': attribute} 
    for attribute, name in athlete_dict.items()
]

all_athletes_options = ["Yes", "No"]
all_athletes_options_radio = [
    {'label':choice, 'value': choice} 
    for choice in all_athletes_options
]

stylesheets = [dbc.themes.MATERIA]
# creates a Dash App
app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

server = app.server  # needed for Heroku to connect to

app.layout = dbc.Container([

    # the first section
    dbc.Card([
        dbc.CardBody([
            html.H1('Sport statistics for global countries',
                    className='card-title text-dark mx-3')
        ])
    ], className="mt-4"),

    # fix sport dropdown and medal radio
    # fix graphs for the sum of medals for each countries in the 120 years
    dbc.Row(className='mt-4', children=[
        dbc.Col(
            # responsivity
            html.P("Choose sport:"), xs="12", sm="12", md="6", lg="4", xl={"size": 1, "offset": 1},
            className="mt-1"
        ),
        dbc.Col(
            dcc.Dropdown(id='sport-dropdown', className='',
                         options=sport_options_dropdown,
                         value='All Sports',
                         placeholder='All Sports'), xs="12", sm="12", md="12", lg="4", xl="3"),

        dbc.Col([
            dbc.Card([
                dcc.RadioItems(id='medal-radio', className="m-1",
                                  options=medal_options,
                                  value='Total'
                               ),
            ])
        ], xs="12", sm="12", md="12", lg='4', xl="3"),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="sum-medals-map"),
            
        ], lg={"size": "6", "offset": 0}, xl={"size": "6", "offset": 0}),


        dbc.Col([
            dcc.Graph(id="sum-medals-top10"),

        ], lg={"size": "6", "offset": 0}, xl={"size": "6", "offset": 0}),
    ]),
    
    ## The second section
    dbc.Card([
        dbc.CardBody([
            html.H1('Sport statistics for global countries over years',
                    className='card-title text-dark mx-3')
        ])
    ], className="mt-4"),


    dbc.Row([
        dbc.Col([
            dcc.Graph(id="medals-graph-world"),
            
        ], lg={"size": "6", "offset": 0}, xl={"size": "6", "offset": 0}),


        dbc.Col([
            dcc.Graph(id="highlights-graph-world"),

        ], lg={"size": "6", "offset": 0}, xl={"size": "6", "offset": 0}),

    
    # the 3rd section
    dbc.Card([
        dbc.CardBody(html.H1("Athlete statistics",
            className='card-title text-dark mx-3'
        ))
    ], className='mt-4'),

    # 2 columns
    dbc.Row([
        # 1st with dropdown menu
        dbc.Col([
            dbc.Card([
                html.H3('Choose a region', className = 'm-2'),
                dcc.Dropdown(
                    id = 'region-dropdown',
                    className = 'm-2',
                    value = "All regions",
                    options = region_options_dropdown
                ),
            ]),
            dbc.Card([
                html.H3('Choose a statistic', className = 'm-2'),
                dcc.RadioItems(
                    id='athlete-radio', 
                    className='m-2',
                    value="Age",
                    options=athlete_options,
                    labelStyle={'display': 'block'}
                ),
            ]),
            dbc.Card([
                html.H3('Choose all athletes', className = 'm-2'),
                dcc.RadioItems(
                    id='total-athletes-radio', 
                    className='m-2',
                    value="No",
                    options=all_athletes_options_radio,
                    labelStyle={'display': 'block'}
                ),
            ]),
        ], lg='6', xl='2'),
        # 2nd with figure
        dbc.Col([
            dcc.Graph(
                id='athlete-distribution-graph',
                className=''
            ),
        ],  lg={"size": "10", "offset": 0}, xl={"size": "10", "offset": 0})
    ], className='mt-4'),


    html.Footer([
        html.H3("120 years of Olympic games", className="h6"),
        html.P("Dashboard av Yuna och Joachim")],
        className="navbar fixed-bottom")

    ]),
    # stores an intermediate value on the clients browser for sharing between callbacks
    dcc.Store(id="filtered-df"),

], fluid=True)



# First section
# when something changes in the input component, the code in function below will run and update the output component
# the components are connected through their id
@app.callback(
    Output("filtered-df", "data"), 
    Input("sport-dropdown", "value")
)
def filter_df(sport):
    """
    Filters the dataframe and stores it intermediary for usage in callbacks
    Returns:
        a dataframe for chosen sport
    """

    # Data for all sports
    if sport=="All Sports":
        df = af.count_medals_n(athlete_iso, "Country", "ISO", "Year")
    # Data for chosen sport
    else:
        df = af.count_medals_n(athlete_iso, "Country", "ISO", "Year", "Sport")
        df = df[df["Sport"]==sport]

    df = df.sort_values(by=["Year", "ISO"])
    
    return df.to_json()


@app.callback(
    [Output("sum-medals-map", "figure"),
    Output("sum-medals-top10", "figure")],
    [Input("filtered-df", "data"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value")],
)

def update_graph(json_df, sport, medal):
    df = pd.read_json(json_df)
    dff= df.groupby(["Country", "ISO"]).sum().reset_index()
    dff = dff.loc[:, ["Country", "ISO", "Gold", "Silver", "Bronze", "Total"]]
   
    fig1 = px.choropleth(dff, locations="ISO",
                        color=medal,
                        scope=None,
                        hover_name="Country",
                        title = f"Geographic map: sum of {sport} {medal} medals", 
                        range_color=[0,dff[medal].quantile(0.95)],
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    fig1["layout"].pop("updatemenus")
        
    temp = dff.sort_values(medal, ascending=False)
    top10_all = temp.head(10)
  
    fig2 = px.bar(top10_all, y="Country", x=medal,
             title=f"top 10 countries by sum of {medal} medals")
     
    return fig1, fig2


# For second section
# sort by country, year
# World-map figure over years
@app.callback(
    [Output("medals-graph-world", "figure"),
    Output("highlights-graph-world", "figure")],
    [Input("filtered-df", "data"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value")]
)
def update_graph(json_df, sport, medal):
    dff = pd.read_json(json_df)
    fig1 = px.choropleth(dff, locations="ISO",
                        color=medal,
                        scope=None,
                        hover_name="Country",
                        animation_frame="Year",
                        title = f"Geographic map: {sport} {medal} medals over years",
                        range_color=[0,dff[medal].quantile(0.95)],
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    fig1["layout"].pop("updatemenus")
        
    temp = dff.sort_values(medal, ascending=False)
    top10_all = temp.head(10)
 
    fig2 = px.bar(top10_all, y="Country", x=medal, color="Year",
             title=f"Hightlights in {sport}: top ten {medal} medals",
             labels={"value":"Number of medals", "variable":"Country"}
             )

    return fig1, fig2


# For 3rd section
# Figure athlete distribution for this chosen sport over age etc.
@app.callback(
    Output("athlete-distribution-graph", "figure"),
    Input("region-dropdown", "value"),
    Input("athlete-radio", "value"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value"),
    Input("total-athletes-radio", "value")
)
def update_graph(chosen_region, athlete_attribute, sport, medal, total_athletes):
    
    
    # Update dataframe after chosen region
    if chosen_region == "All regions" and sport=="All Sports":
        df_sport = athlete_regions.copy()
    elif chosen_region == "All regions" and sport!="All Sports":
        df_sport = athlete_regions[athlete_regions["Sport"] == sport]
    elif chosen_region != "All regions" and sport=="All Sports":
        df_sport = athlete_regions[athlete_regions["region"] == chosen_region]
    else:
        df_sport = athlete_regions[athlete_regions["region"] ==chosen_region] 
        df_sport = df_sport[df_sport["Sport"] == sport]
    
    # medal
    if total_athletes == "Yes":
        df_athlete = df_sport.copy()
    elif medal!="Total":
        df_athlete = df_sport[df_sport["Medal"]==medal]
    else:
        df_athlete = df_sport[(df_sport["Medal"]=="Gold") | (df_sport["Medal"]=="Silver") | (df_sport["Medal"]=="Bronze")] 

    df_athlete = df_athlete[df_athlete[athlete_attribute].notna()]

    # plot:
    athlete_counts = df_athlete[athlete_attribute].value_counts()
    fig = px.bar(athlete_counts, title=f"{athlete_attribute} of {medal} medals winners or athletes({total_athletes})")
    fig.update_layout(
        xaxis_title = unit_dict[athlete_attribute],
        yaxis_title = "Frequency",
        title_x = 0.5, 
        #showlegend = False
    )
    
    return fig



if __name__ == '__main__':
    app.run_server(debug= True)
