# Main: contains side board and calls the two dashboards.
# Based on
# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/page-2
"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""

import pandas as pd

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import plotly_express as px

import analyze_functions as af

# Set both overall settings and sidebar settings
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

# needed for Heroku to connect to
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("OS-Project", className="display-5"),
        html.Hr(),
        html.P(
            "Yuna Liu and Joachim Wiegert", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Canada medals", href="/page-1", active="exact"),
                dbc.NavLink("Canada top statistics", href="/page-2", active="exact"),
                dbc.NavLink("Canada athletes", href="/page-3", active="exact"),
                dbc.NavLink("Worldwide 1", href="/page-4", active="exact"),
                dbc.NavLink("Worldwide 2", href="/page-5", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Import data
df_orig = pd.read_csv("data/canada.csv")
athlete_regions = pd.read_csv("data/athlete_regions.csv")
noc_iso = pd.read_csv("data/noc_iso.csv")
noc_iso = noc_iso.iloc[:, 1:]


# Settings for Canada statistics
# Medal options
medal_list = "Gold Silver Bronze Total".split()
medal_options = [{'label': medal, 'value': medal} for medal in medal_list]

# Medal-Time slider options 
slider_marks = {
    str(year): str(year) for year in range(
        df_orig["Year"].min(), df_orig["Year"].max(), 10
    )
}

# Attribute dropdown options
attr_dict = {
    'Sport':'Sport', 
    'Event':'Sport event', 
    'Games':'Year & Season',
    'Season':'Season', 
    'Name':'Athlete', 
    'Sex':'Athlete gender', 
    'Age':'Athlete age',
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

# Set initial dataframe for figure1, medal-time-figure
df_medal = af.count_medals_n(df_orig, "Year")


# TODO all functions, callbacks and pages for international data

# Settings for international data
# Set initial settings
# Data for all sports
df_int = af.count_medals_n(athlete_regions, "NOC", "Year")
df_int = df_int.reset_index()
df_iso = df_int.merge(noc_iso, on="NOC", how="left")
df_iso = df_iso.sort_values(by=["Year", "NOC"])

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








@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def render_page_content(pathname):

    if pathname == "/page-1":
        return [
            # Main Title
            dbc.Card([
                dbc.CardBody(html.H1(
                    'Canada in 120 years of Olympic history',
                    className='text-primary-m-3'
                ))
            ], className='mt-3'),

            # Figure for medals per year
            # 2 columns,
            dbc.Row([

                #  1st col: with medal picker and with numbers to the right
                dbc.Col([
                    dbc.Card([
                        html.H3('Choose a medal:', className='m-2'),
                        dcc.RadioItems(
                            id='medal-picker-radio', 
                            className='m-2',
                            value="Total",
                            options=medal_options,
                            labelStyle={'display': 'block'}
                        )
                    ]),
                    dbc.Card([
                        dbc.Row([
                            html.H3(
                                "Number of medals shown",
                                className='m-2'
                            ),
                            dbc.Col([
                                html.P("Total:", className='m-2'),
                                html.P("Gold:", className='m-2'),
                                html.P("Silver:", className='m-2'),
                                html.P("Bronze:", className='m-2'),
                            ]),
                            dbc.Col([
                                html.P(id='total-medals', className='m-2'),
                                html.P(id='gold-medals', className='m-2'),
                                html.P(id='silver-medals', className='m-2'),
                                html.P(id='bronze-medals', className='m-2'),
                            ])
                        ])
                    ], className='mt-1')
                ], lg='8', xl='2'),
                #  2nd col: with figure
                dbc.Col([
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
                ]),
            ], className='mt-4')
        ]

    # canada top statistiscs
    elif pathname == "/page-2":
        return [
            # Main Title (top statistics)
            dbc.Card([
                dbc.CardBody(html.H1(
                    'Canada in 120 years of Olympic history',
                    className='text-primary-m-3'
                ))
            ], className='mt-3'),

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
                        id='top10-graph',
                        className=''
                    ),
                ])
            ], className='mt-4'),
        ]


    elif pathname == "/page-3":
        return [
            # Main Title (athlete statistics)
            dbc.Card([
                dbc.CardBody(html.H1(
                    'Canada in 120 years of Olympic history',
                    className='text-primary-m-3'
                ))
            ], className='mt-3'),
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
        ]

    elif pathname == "/page-4":
        return [
            dbc.Card([
                dbc.CardBody([
                    html.H1(
                        'Global countries in 120 years of Olympic history',
                        className='card-title text-dark mx-3')
                ])
            ], className="mt-4"),
        ]

    elif pathname == "/page-5":
        return [
            dbc.Card([
                dbc.CardBody([
                    html.H1(
                        'Global countries in 120 years of Olympic history',
                        className='card-title text-dark mx-3')
                ])
            ], className="mt-4"),
        ]




    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# Callbacks and functions


@app.callback(
    Output("medals-graph", "figure"),
    Output("gold-medals", "children"),
    Output("silver-medals", "children"),
    Output("bronze-medals", "children"),
    Output("total-medals", "children"),
    Input("medal-picker-radio", "value"),
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
    df_medal = af.count_medals_n(df_orig, "Year", "Season")

    # Set time range
    dff = df_medal[
        (df_medal[df_medal.columns[0]] >= time_index[0]) & 
        (df_medal[df_medal.columns[0]] <= time_index[1])
    ]
    
    # Save total number of medals shown
    number_medals = [dff[medal].sum() for medal in medal_list]
    
    # Update figure
    # title=f"The number of {medal} medals from {time_index[0]} to {time_index[1]}",
    fig = px.bar(
        dff, x="Year", y=medal, color="Season",
        labels={"value":"Number medals", "variable":"Medal"}
    )

    for data in fig.data:
        data["width"]= 0.5
    # when user choose a time_index to a small range, t.ex, 5 years,
    # the bar width is so large that spread to the year before and the year after
    # the bar width need to be smaller
    # http://www.programshelp.com/help/python/Increase__bar_width___px_bar_.html

    return fig, number_medals[0], number_medals[1], number_medals[2], number_medals[3]



# Figure showing top10-statistics for Canada
@app.callback(
    Output("top10-graph", "figure"),
    Input("attribute-dropdown", "value"),
)
def update_graph(chosen_attribute):
    """
    Figure with top-best for Canada
    """
    # Update df_medal after what is chosen
    df_top = af.count_medals_n(df_orig, chosen_attribute)

    # Sort by attribute and extract top 10
    df_top = df_top.sort_values("Total", ascending=False)
    df_top = df_top.head(10)

    # Update figure
    fig = px.bar(
        df_top, x=chosen_attribute, y=medal_list,
        title=f"Canada, top {attr_dict[chosen_attribute]}",
        labels={"value":"Number medals", "variable":"Medal"}
    )
    fig.update_layout(barmode='group', xaxis_tickangle=45)

    return fig



# Histograms with Canadian athletes statistics
@app.callback(
    Output("athlete-graph", "figure"),
    Input("athlete-radio", "value"),
    Input("gender-picker-radio", "value")
)
def update_graph(athlete_attribute, athlete_gender):
    """
    Figure with statistics for athletes
    """

    # Update figure (according to chosen gender)
    if athlete_gender == "Both":
        fig = px.histogram(df_orig, x=athlete_attribute)
    else:
        fig = px.histogram(df_orig[df_orig["Sex"]==athlete_gender], x=athlete_attribute)
    
    # Update axis texts
    fig.layout.yaxis.title.text = "Number of athletes"
    fig.layout.xaxis.title.text = unit_dict[athlete_attribute]

    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(port=8888)