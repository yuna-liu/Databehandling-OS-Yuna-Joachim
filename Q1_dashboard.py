import pandas as pd
from dash import dcc, html
import dash
from load_data import ShowMeData
from dash.dependencies import Output, Input
import plotly_express as px
import plotly.graph_objects as go
from time_filtering import filter_time

# 1. Import data
df = pd.read_csv("data/canada.csv")
df_canada = pd.DataFrame(df.groupby(["Year", "Medal"]).count()["ID"]).reset_index()

# use df.pivot() for long-to-wide
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html#pandas.DataFrame.pivot
df_medal = df_canada.pivot(index="Year", columns="Medal", values="ID")
df_medal.fillna(0, inplace=True)
df_medal.reset_index(drop=False, inplace=True )
df_medal["Total"] = df_medal["Bronze"] + df_medal["Gold"] + df_medal["Silver"]
df_medal = df_medal.astype("int32")
df_medal.head(10)

# Initiate dashboard

medal_options_dropdown = [{'label': medal, 'value': medal}
                          for medal in "Bronze Gold Silver Total".split()]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Canada in 120 years of Olympic history: athletes and results'),
    html.H2('Choose a medal:'),
    dcc.Dropdown(id='medal-picker-dropdown', className='',
                 value="Total",
                 options=medal_options_dropdown),
    dcc.Graph(id='medals-graph', className=''),
])


@app.callback(Output("medals-graph", "figure"),
              Input("medal-picker-dropdown", "value")
              )
              
def update_graph(medal):
    
    fig = px.line(df_medal, x="Year", y=medal, title=f"The number of {medal}s from Athens 1896 to Rio 2016")
    
    return fig
    

if __name__ == '__main__':
    app.run_server(debug= True)