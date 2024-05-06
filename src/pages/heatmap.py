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
    path="/heatmap",
    title="Heatmap"
)

athlete_events_df = pd.read_csv("./assets/athlete_events.csv")
noc_regions_df = pd.read_csv("./assets/noc_regions.csv")

BINS = 24

# Create bins for height and weight
height_weight_medal_df = athlete_events_df.copy()
height_weight_medal_df = height_weight_medal_df.dropna(subset=["Height", "Weight"])
height_weight_medal_df["Height Bin"] = pd.cut(height_weight_medal_df["Height"], bins=BINS)
height_weight_medal_df["Weight Bin"] = pd.cut(height_weight_medal_df["Weight"], bins=BINS)

# Group by sports, separated by sex
height_weight_medal_df = height_weight_medal_df.groupby(["Sport", "Sex", "Height Bin", "Weight Bin"], observed=False)["Medal"].count().reset_index(name="Medal Count")

# Create pivot tables for each sport and sex
sports_df_list = {}
for (col, sport) in height_weight_medal_df.groupby("Sport"):
    sports_df_list[col] = {}
    for (c, sex) in sport.groupby("Sex"):
        sports_df_list[col][c] = pd.pivot_table(sex, index="Height Bin", columns="Weight Bin", values="Medal Count", observed=False).fillna(0)
for sport in sports_df_list.keys():
    for sex in sports_df_list[sport]:
        sports_df_list[sport][sex].columns = sports_df_list[sport][sex].columns.astype(str)
        sports_df_list[sport][sex].index = sports_df_list[sport][sex].index.astype(str)
        
# Create heatmap subplot figure
heatmap_fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=("Females", "Males"),
    shared_yaxes=True
)

# Starting heatmap
heatmap_fig.add_trace(
    go.Heatmap(
        x=sports_df_list["Alpine Skiing"]["F"].columns,
        y=sports_df_list["Alpine Skiing"]["F"].index,
        z=sports_df_list["Alpine Skiing"]["F"].values,
        visible=True,
        hovertemplate=
            "<b>Height Bin:</b> %{y}cm<br>" +
            "<b>Weight Bin:</b> %{x}kg<br>" +
            "<b>Total Medals Won:</b> %{z}",
        name="",
        coloraxis="coloraxis"
    ),
    row=1,
    col=1
)
heatmap_fig.add_trace(
    go.Heatmap(
        x=sports_df_list["Alpine Skiing"]["M"].columns,
        y=sports_df_list["Alpine Skiing"]["M"].index,
        z=sports_df_list["Alpine Skiing"]["M"].values,
        visible=True,
        hovertemplate=
            "<b>Height Bin:</b> %{y}cm<br>" +
            "<b>Weight Bin:</b> %{x}kg<br>" +
            "<b>Total Medals Won:</b> %{z}",
        name="",
        coloraxis="coloraxis"
    ),
    row=1,
    col=2
)
heatmap_fig.update_layout(
    title="Total Medals Won by Height and Weight in Alpine Skiing, Separated by Gender"
)

# Add heatmap traces for each sport
for i, sport in enumerate(sports_df_list.keys()):
    for j, sex in enumerate(sports_df_list[sport]):
        heatmap_fig.add_trace(
            go.Heatmap(
                x=sports_df_list[sport][sex].columns,
                y=sports_df_list[sport][sex].index,
                z=sports_df_list[sport][sex].values,
                visible=False,
                hovertemplate=
                    "<b>Height Bin:</b> %{y}cm<br>" +
                    "<b>Weight Bin:</b> %{x}kg<br>" +
                    "<b>Total Medals Won:</b> %{z}",
                name="",
                coloraxis="coloraxis"
            ),
            row=1,
            col=j + 1
        )

# Create dropdown option for each sport
sports_options = []
for i, key in enumerate(sports_df_list.keys()):
    visible_list = [False] * (len(sports_df_list.keys()) + 2) * 2
    visible_list[i * 2 + 2] = True
    visible_list[i * 2 + 3] = True
    sports_options.append(dict(
        label=key,
        method="update",
        args=[
            {"visible":visible_list},
            {"title":f"Total Medals Won by Height and Weight in {key}, Separated by Gender"}
        ]
    ))
    
heatmap_fig.update_layout(
    width=1000,
    height=550,
    autosize=False,
    coloraxis=dict(
        colorscale="thermal",
        colorbar=dict(
            title="Medals Won"
        )
    ),
    updatemenus=[dict(
        active=0,
        buttons=sports_options,
        x=1.2,
        y=1.2
    )]
)

heatmap_fig.update_xaxes(
    title_text="Weight (kg)",
    row=1,
    col=1
)
heatmap_fig.update_xaxes(
    title_text="Weight (kg)",
    row=1,
    col=2
)
heatmap_fig.update_yaxes(
    title_text="Height (cm)",
    row=1,
    col=1
)

layout = html.Div([
    dcc.Graph(
        id="heatmap",
        figure=heatmap_fig
    )
])