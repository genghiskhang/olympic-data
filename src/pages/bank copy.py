from dash import Dash, html, dcc, callback, Output, Input, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

import json

register_page(
    __name__,
    path="/bank",
    title="Bank"
)

athlete_events_df = pd.read_csv("./assets/athlete_events.csv")
noc_regions_df = pd.read_csv("./assets/noc_regions.csv")

medals_won_df = athlete_events_df.drop_duplicates(subset=["NOC", "Games", "Year", "Season", "City", "Sport", "Event"])
medals_won_df = athlete_events_df.merge(noc_regions_df, on="NOC", how="left")
medals_won_df = medals_won_df.groupby(["Year", "region"])["Medal"].count().reset_index(name="Won")
medals_won_df

medals_attempted_df = athlete_events_df.drop_duplicates(subset=["NOC", "Games", "Year", "Season", "City", "Sport", "Event"])
medals_attempted_df = athlete_events_df.merge(noc_regions_df, on="NOC", how="left")
medals_attempted_df["Medal"] = medals_attempted_df["Medal"].fillna("None")
medals_attempted_df = medals_attempted_df.groupby(["Year", "region"])["Medal"].count().reset_index(name="Attempted")

success_rate_df = medals_won_df.merge(medals_attempted_df, on=["Year", "region"], how="left")
success_rate_df["Success Rate"] = success_rate_df["Won"] / success_rate_df["Attempted"]

success_rate_df

success_rate_df['Cumulative Success'] = medals_won_df.groupby('region')['Won'].transform(pd.Series.cumsum)

first_year = medals_won_df['Year'].min()
last_year = medals_won_df['Year'].max()
final_year_data = medals_won_df[medals_won_df['Year'] == last_year]
average_cumulative_medals = final_year_data['Cumulative Wins'].mean()

average_line = pd.DataFrame({
    "Year": [first_year, last_year],
    "Cumulative Wins": [0, average_cumulative_medals],
    "region": ["Average"] * 2
})

print(medals_won_df)

bank_fig = px.line(medals_won_df, x = "Year", y = "Cumulative Wins", color = 'region',
        width=600, height=450)

bank_fig_after = px.line(medals_won_df, x = "Year", y = "Cumulative Wins", color = 'region',
        width=600, height=450)

print(average_cumulative_medals)

average_trace = go.Scatter(
    x=[first_year, last_year],
    y=[0, average_cumulative_medals],
    mode='lines',
    line=dict(dash='dash', color='black'),
    name='Average'
)
bank_fig_after.add_trace(average_trace)

layout = html.Div([
    html.Div([
        dcc.Graph(
            id="bank",
            figure=bank_fig, 
            style={'display': 'inline-block', 'width': '49%'}
        ),
        dcc.Graph(
            id="bank2",
            figure=bank_fig_after, 
            style={'display': 'inline-block', 'width': '49%'},
        ),
    ]),
    html.P("""Before and After results of applying automatic scaling axis banking to a subgraph.""")
])