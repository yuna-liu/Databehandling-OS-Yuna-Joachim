import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly_express as px

import analyze_functions as af


# Import data
df = pd.read_csv("data/canada.csv")

# Column names
# ['Unnamed: 0', 'ID', 'Name', 'HashName', 'Sex', 'Age', 'Height',
#       'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport',
#       'Event', 'Medal']


# Medal options
medal_list = "Gold Silver Bronze Total".split()
medal_options = [{'label': medal, 'value': medal} for medal in medal_list]

# Medal-Time slider options 
slider_marks = {
    str(year): str(year) for year in range(
        df["Year"].min(), df["Year"].max(), 10
    )
}

# Set dataframe for figure1, medal-time-figure
df_medal = af.count_medals_n(df, "Year")


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


# Set theme settings
stylesheets = [dbc.themes.MATERIA]

# Initiate dashboard
#app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=stylesheets,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")]
)


app.layout = dbc.Container([

    # Main Title
    dbc.Card([
        dbc.CardBody(html.H1(
            'Canada in 120 years of Olympic history: athletes and results',
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
    ], className='mt-4'),

    # 2nd Title, for second figure
    dbc.Card([
        dbc.CardBody(html.H1("Top statistics for Canada",
            className='text-primary-m-4'
        ))
    ], className='mt-5'),

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

    # 3rd title, for histograms
    dbc.Card([
        dbc.CardBody(html.H1("Athlete statistics",
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
])

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
    df_medal = af.count_medals_n(df, "Year", "Season")

    # Set time range
    dff = df_medal[
        (df_medal[df_medal.columns[0]] >= time_index[0]) & 
        (df_medal[df_medal.columns[0]] <= time_index[1])
    ]
    
    # Save total number of medals shown
    number_medals = [dff[medal].sum() for medal in medal_list]
    
    # Update figure
    fig = px.bar(
        dff, x="Year", y=medal, color="Season",
        title=f"The number of {medal} medals from {time_index[0]} to {time_index[1]}",
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
    df_top = af.count_medals_n(df, chosen_attribute)

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
        fig = px.histogram(df, x=athlete_attribute)
    else:
        fig = px.histogram(df[df["Sex"]==athlete_gender], x=athlete_attribute)
    
    # Update axis texts
    fig.layout.yaxis.title.text = "Number of athletes"
    fig.layout.xaxis.title.text = unit_dict[athlete_attribute]

    return fig


if __name__ == '__main__':
    app.run_server(debug= True)
