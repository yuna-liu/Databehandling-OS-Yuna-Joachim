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
        dbc.CardBody(html.H1("Top (10) - statistics for global countries",
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
                dcc.Dropdown(
                    id = 'attribute-dropdown',
                    className = 'm-2',
                    value = "Sport",
                    options = attribute_options_dropdown
                ),
            ])
        ], lg='8', xl='2'),
        # 2nd with figure
        dbc.Col([
            dcc.Graph(
                id='top10-graph',
                className=''
            ),
        ])
    ], className='mt-4'),

    # The 4th section: for age histograms 
    # and other histograms of atheletes
    dbc.Card([
        dbc.CardBody(html.H1("Sport statistics for athletes",
            className='text-primary-m-4'
        ))
    ]),

    # two columns
    dbc.Row([
        dbc.Col([
            dbc.Card([
            # 1st with dropdown menu
                html.H3('Choose a gender', className = 'm-2'),
                dcc.RadioItems(
                    id='gender-picker-radio', 
                    className='m-2',
                    value="Both",
                    options=gender_options,
                    labelStyle={'display': 'block'}
                ),

                html.H3('Choose a statistic', className = 'm-2'),
                dcc.RadioItems(
                    id='athlete-radio', 
                    className='m-2',
                    value="Age",
                    options=athlete_options,
                    labelStyle={'display': 'block'}
                ),
            ], className='mt-1'),
        ], lg='8', xl='3'),
        # 2nd with figure
        dbc.Col([
            dcc.Graph(
                id='athlete-graph',
                className=''
            ),
        ])
    ], className='mt-4'),

    html.Footer([
        html.H3("120 years of Olympic games", className="h6"),
        html.P("Dashboard av Yuna och Joachim")],
        className="navbar fixed-bottom")

    ]),
    # stores an intermediate value on the clients browser for sharing between callbacks
    dcc.Store(id="filtered-df"),

], fluid=True)




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

    return df.to_json()


@app.callback(
    Output("sum-medals-map", "figure"),
    Output("sum-medals-top10", "figure"),
    Input("filtered-df", "data"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value"),
)

def update_graph(json_df, sport, medal):
    df = pd.read_json(json_df)
    dff= df.groupby(["Country", "ISO"]).sum().reset_index()
    dff = dff.loc[:, ["Country", "ISO", "Gold", "Silver", "Bronze", "Total"]]
   
    fig1 = px.choropleth(dff, locations="ISO",
                        color=medal,
                        scope=None,
                        hover_name="Country",
                        title = f"Geographic map on sum of {medal} medals in {sport} games", 
                        range_color=[0,dff[medal].quantile(0.95)],
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    fig1["layout"].pop("updatemenus")
        
    temp = dff.sort_values(medal, ascending=False)
    top10_all = temp.head(10)
  
    fig2 = px.bar(top10_all, y="Country", x=medal,
             title=f"top 10 countries by sum of {medal} medals")
     
    return fig1, fig2


# sort by country, year
# World-map figure over years
@app.callback(
    Output("medals-graph-world", "figure"),
    Output("highlights-graph-world", "figure"),
    Input("filtered-df", "data"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value")
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


# Figure showing top10-statistics for global countries
@app.callback(
    Output("top10-graph", "figure"),
    Input("region-dropdown", "value"),
    Input("attribute-dropdown", "value"),
    Input("sport-dropdown", "value"),
    Input("medal-radio", "value")
)
def update_graph(chosen_region, chosen_attribute, sport, medal):
    # Update dataframe after chosen region
    if chosen_region == "All regions":
        df_top = af.count_medals_n(athlete_regions, chosen_attribute)
    else:
        athlete_region = athlete_regions[athlete_regions['region']==chosen_region]
        df_top = af.count_medals_n(athlete_region, chosen_attribute)

    # Sort by attribute and extract top 10
    df_top = df_top.sort_values("Total", ascending=False)
    df_top = df_top.head(10)

    # Update figure
    fig = px.bar(
        df_top, x=chosen_attribute, y=medal_list, 
        title=f"{chosen_region}: top {attr_dict[chosen_attribute]}",
        labels={"value":"Number of medals", "variable":"Medal"}
    )
    fig.update_layout(barmode='group', xaxis_tickangle=45)

    return fig


# Histograms with athletes statistics in each country
@app.callback(
    Output("athlete-graph", "figure"),
    Input("region-dropdown", "value"),
    Input("athlete-radio", "value"),
    Input("gender-picker-radio", "value")
)
def update_graph(chosen_region, athlete_attribute, athlete_gender):
    """
    Figure with statistics for athletes
    """

    # Update dataframe after chosen region
    if chosen_region == "All regions":
        athlete_region = athlete_regions.copy()
    else:
        athlete_region = athlete_regions[athlete_regions['region']==chosen_region]

    # Update figure (according to chosen gender)
    if athlete_gender == "Both":
        fig = px.histogram(athlete_region, x=athlete_attribute)
    else:
        fig = px.histogram(athlete_region[athlete_region["Sex"]==athlete_gender], x=athlete_attribute)
    
    # Update axis texts
    fig.layout.yaxis.title.text = "Number of athletes"
    fig.layout.xaxis.title.text = unit_dict[athlete_attribute]

    return fig


if __name__ == '__main__':
    app.run_server(debug= True)
