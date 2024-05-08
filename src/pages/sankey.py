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
performance_df["Medal"] = performance_df["Medal"].fillna("None")

# Filter out data to get all participants that played in at least FIRST_N_GAMES
performance_df = performance_df.groupby(["Name", "Year", "Medal"])["Medal"].count().reset_index(name="Medal Count")
performance_df = performance_df.groupby(["Name"]).filter(lambda x: x["Year"].nunique() > FIRST_N_GAMES)
performance_df["Appearance"] = performance_df.sort_values(by="Year").groupby("Name")["Year"].rank(method="first").astype(int)
performance_df = performance_df[performance_df["Appearance"] <= FIRST_N_GAMES]

# Get the highest medal earned by the athlete for each year
def highest_medal(medals):
    if "Gold" in medals:
        return "Gold"
    elif "Silver" in medals:
        return "Silver"
    elif "Bronze" in medals:
        return "Bronze"
    else:
        return "None"
performance_df = performance_df.groupby(["Name", "Appearance"])["Medal"].agg(list).reset_index()
performance_df["Highest"] = performance_df["Medal"].apply(highest_medal)
performance_df["Source"] = performance_df.apply(lambda x: f"Year {x['Appearance']} {x['Highest']}", axis=1) 

# Get the source and target positions for sankey diagram
performance_df["Total Medals"] = 1
medal_map = {"None":0, "Bronze":1, "Silver":2, "Gold":3}
performance_df["Source"] = performance_df.apply(lambda x: medal_map[x['Highest']] + x['Appearance'] * len(medal_map) - len(medal_map), axis=1)
performance_df["Next Medal"] = performance_df.groupby(["Name"])["Highest"].shift(-1)
def get_target(row):
    if pd.notna(row["Next Medal"]) and row["Appearance"] < FIRST_N_GAMES:
        return medal_map[row["Next Medal"]] + (row["Appearance"]) * len(medal_map)
    else:
        return np.nan
performance_df["Target"] = performance_df.apply(get_target, axis=1)
color_map = {"None":"#444444", "Bronze":"#CD7F32", "Silver":"#C0C0C0", "Gold":"#D4AF37"}
performance_df["Color"] = performance_df.apply(lambda x: color_map[x["Highest"]], axis=1)

# Aggregate the data back into groups by the year and medals earned, as well as source and target
performance_df = performance_df.groupby(["Appearance", "Highest", "Source", "Target", "Color"])["Total Medals"].sum().reset_index(name="Total Medals")

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
    ),
    html.P("""A Sankey diagram that shows the progression of veteran olympic athletes. For example, 
           it will show the number of first time athletes that won a bronze medal in their first game 
           and a silver medal in their second game and so on. It allows the user to see how an 
           aggregated number of athletes performed each time they participated in the Olympic games 
           through the hover feature.""")
])