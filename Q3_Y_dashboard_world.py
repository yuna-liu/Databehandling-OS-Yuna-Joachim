import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly_express as px
import plotly.graph_objects as go

import analyze_functions as af
import sub_df as af2

# Import data
athlete_regions = pd.read_csv("data/athlete_regions.csv")
noc_iso = pd.read_csv("data/noc_iso.csv")
noc_iso = noc_iso.iloc[:, 1:]

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
            html.H1('Global countries in 120 years of Olympic history: sports and results',
                    className='card-title text-dark mx-3')
        ])
    ], className="mt-4"),

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
            dcc.Graph(id="medals-graph"),
            
        ], lg={"size": "6", "offset": 1}, xl={"size": "6", "offset": 1}),

        dbc.Col([
            dbc.Row(
                dbc.Card([
                    html.H2("Summary", className="h5 mt-3 mx-3"),
                    html.P(id="sum-medals", className="text-success h1 mx-2")
                ]), className="mt-5 h-25"
            ),
            # dbc.Row(
            #     dbc.Card([
            #         html.H2("Top athletes", className="h5 mt-3 mx-3"),
            #         #html.P(id="lowest-value", className="text-danger h1 mx-2")
            #     ]),
            #     className="mt-5 h-25"
            # ),
        ], sm="5", md="3", lg="3", xl="2", className="mt-5 mx-5"),

    # 2nd Title, for second figure
    dbc.Card([
        dbc.CardBody(html.H1("Top (20) - statistics for global countries",
            className='card-title text-dark mx-3'
        ))
    ], className='mt-4'),

    # 2 columns
    dbc.Row([
        # 1st with dropdown menu
        dbc.Col([
            html.H3('Choose a statistic', className = 'm-2'),
            dcc.Dropdown(
                id = 'attribute-dropdown',
                className = 'm-2',
                value = "Sport",
                options = attribute_options_dropdown
            ),
        ], lg='8', xl='2'),
        # 2nd with figure
        dbc.Col([
            dcc.Graph(
                id='top20-graph',
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



@app.callback(Output("filtered-df", "data"), Input("sport-dropdown", "value")
              )

def filter_df(sport):
    """Filters the dataframe and stores it intermediary for usage in callbacks
    Returns:
        a dataframe for chosen sport
    """
    # Data for all sports
    if sport=="All Sports":
        dff = df_iso
    # Data for chosen sport
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
    Output("sum-medals", "children"),
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

    # Save total number of medals in the history
    sum_medals = f"{chosen_sport} {medal} Medals: {dff[medal].sum()}"

    return fig, sum_medals


# Figure showing top20-statistics for global countries
@app.callback(
    Output("top20-graph", "figure"),
    Input("attribute-dropdown", "value"),
)
def update_graph(chosen_attribute):
    # Update df_medal after what is chosen
    df_top = af.count_medals_n(athlete_regions, chosen_attribute)

    # Sort by attribute and extract top 10
    df_top = df_top.sort_values("Total", ascending=False)
    df_top = df_top.head(20)

    # Update figure
    fig = px.bar(
        df_top, x=chosen_attribute, y=medal_list,
        title=f"Canada, top {attr_dict[chosen_attribute]}",
        labels={"value":"Number medals", "variable":"Medal"}
    )
    fig.update_layout(barmode='group', xaxis_tickangle=45)

    return fig



if __name__ == '__main__':
    app.run_server(debug= True)
