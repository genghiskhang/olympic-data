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
    path="/heatmap",
    title="Heatmap"
)

athlete_events_df = pd.read_csv("./assets/athlete_events.csv")
noc_regions_df = pd.read_csv("./assets/noc_regions.csv")

# Group medal counts by height and weight
height_weight_medal_df = athlete_events_df.dropna(subset=["Height", "Weight"])
height_weight_medal_df = height_weight_medal_df.groupby(["Sport", "Height", "Weight"])["Medal"].count().reset_index(name="Medal Count")

# List of medal counts by height and weight for each sport
sports_df_list = {col:pd.pivot_table(sport, index="Height", columns="Weight", values="Medal Count").fillna(0) for (col, sport) in height_weight_medal_df.groupby("Sport")}

# Heatmap figure
heatmap_fig = go.Figure(
    data=go.Heatmap(
        x=sports_df_list["Alpine Skiing"].columns,
        y=sports_df_list["Alpine Skiing"].index,
        z=sports_df_list["Alpine Skiing"].values,
        visible=True,
        hovertemplate=
            "<b>%{x}cm-%{y}kg</b><br>" +
            "Total Medals Won: %{z}<br>"
    )
)
heatmap_fig.update_layout(
    title="Total Medals Won by Height and Weight in Alpine Skiing"
)

# Add heatmap traces for each sport
for key in sports_df_list.keys():
    heatmap_fig.add_traces(
        data=go.Heatmap(
            x=sports_df_list[key].columns,
            y=sports_df_list[key].index,
            z=sports_df_list[key].values,
            visible=False,
            hovertemplate=
                "<b>%{x}kg-%{y}cm</b><br>" +
                "Total Medals Won: %{z}<br>"
        )
    )

# Create dropdown option for each sport
sports_options = []
for i, key in enumerate(sports_df_list.keys()):
    visible_list = [False] * len(sports_df_list.keys())
    visible_list[i] = True
    
    sports_options.append(dict(
        label=key,
        method="update",
        args=[
            {"visible":visible_list},
            {"title":f"Total Medals Won by Height and Weight in {key}"}
        ]
    ))
heatmap_fig.update_layout(
    width=800,
    height=600,
    autosize=False,
    xaxis=dict(title="Weight (kg)"),
    yaxis=dict(title="Height (cm)"),
    coloraxis=dict(
        colorbar=dict(
            title="Medals Won"
        )
    ),
    updatemenus=[dict(
        active=0,
        buttons=sports_options
    )]
)

layout = html.Div([
    dcc.Graph(
        id="heatmap",
        figure=heatmap_fig
    )
])