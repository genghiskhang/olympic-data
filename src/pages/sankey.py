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

athlete_events_df = pd.read_csv("./assets/athlete_events.csv")
noc_regions_df = pd.read_csv("./assets/noc_regions.csv")

FIRST_N_GAMES = 4
performance_df = athlete_events_df.copy()
performance_df = performance_df.dropna(subset=["Name", "Year"])
performance_df = performance_df.groupby(["Name", "Year", "Medal"])["Medal"].count().reset_index(name="Medal Count")
performance_df = performance_df.groupby(["Name"]).filter(lambda x: x["Year"].nunique() > FIRST_N_GAMES)
performance_df["Appearance"] = performance_df.sort_values(by="Year").groupby("Name")["Year"].rank(method="first").astype(int)
performance_df = performance_df[performance_df["Appearance"] <= FIRST_N_GAMES]
performance_df = performance_df.groupby(["Medal", "Appearance"])["Medal Count"].sum().reset_index(name="Medal Count")
performance_df["Source"] = performance_df["Appearance"] - 1
performance_df["Target"] = performance_df.apply(lambda x: x["Source"] + 1, axis=1)
color_map = {"Bronze":"#CD7F32", "Silver":"#C0C0C0", "Gold":"#D4AF37"}
performance_df["Color"] = performance_df.apply(lambda x: color_map[x["Medal"]], axis=1)
order_map = {"Bronze":0, "Silver":1, "Gold":2}
performance_df = performance_df.sort_values(by="Medal", key=lambda x: x.map(order_map))

labels = ["First Game", "Second Game", "Third Game", "Fourth Game", "END"]

sankey_fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = labels
    ),
    link = dict(
        arrowlen=15,
        source = performance_df["Source"],
        target = performance_df["Target"],
        value = performance_df["Medal Count"],
        color = performance_df["Color"]
    )
)])

sankey_fig.update_layout(title_text="Flow of Performance of Athletes over their First Four Games")

layout = html.Div([
    dcc.Graph(
        id="sankey",
        figure=sankey_fig
    )
])