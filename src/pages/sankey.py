from dash import Dash, html, dcc, callback, Output, Input, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

import json

register_page(
    __name__,
    path="/sankey",
    title="Sankey"
)

performance_df = pd.read_csv('./datasets/performance_flow_clean.csv')

FIRST_N_GAMES = 4
labels = []
for i in range(1, FIRST_N_GAMES + 1):
    labels.append(f"Year {i} None")
    labels.append(f"Year {i} Bronze")
    labels.append(f"Year {i} Silver")
    labels.append(f"Year {i} Gold")
    
colors = ["#444444", "#CD7F32", "#C0C0C0", "#D4AF37"] * FIRST_N_GAMES

sankey_fig = go.Figure(data=[go.Sankey(
    arrangement = "fixed",
    node = dict(
        pad = 20,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = labels,
        color = colors,
        hovertemplate="%{value} Athletes from %{label}<extra></extra>"
    ),
    link = dict(
        source = performance_df["Source"],
        target = performance_df["Target"],
        value = performance_df["Total Medals"],
        color = performance_df["Color"],
        hovertemplate="Total of %{value} Athletes from %{source.label} to %{target.label}<extra></extra>"
    )
)])

sankey_fig.update_layout(
    width=1000,
    height=600,
    title_text=f"Highest Medal Earned by Athletes over their First {FIRST_N_GAMES} Games"
)

layout = html.Div([
    dcc.Graph(
        id="sankey",
        figure=sankey_fig
    )
])