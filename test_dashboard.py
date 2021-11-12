import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group")

# Data for the tip-graph
df_tip = px.data.tips()

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([ 
        dcc.Graph(id='tip-graph'),
        html.Label([
            "colorscale",
            dcc.Dropdown(
                id='colorscale-dropdown', clearable=False,
                value='bluyl', options=[
                    {'label': c, 'value': c}
                    for c in px.colors.named_colorscales()
                ])
        ]),
    ])
])

# Callback function that automatically updates the tip-graph based on chosen colorscale
@app.callback(
    Output('tip-graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_tip_figure(colorscale):
    return px.scatter(
        df_color, x="total_bill", y="tip", color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl", title="Tips"
    )

if __name__ == '__main__':
    app.run_server(debug=True)