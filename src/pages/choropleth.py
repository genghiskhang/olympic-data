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
    path="/choropleth",
    title="Choropleth"
)

athlete_events_df = pd.read_csv("./assets/athlete_events.csv")
noc_regions_df = pd.read_csv("./assets/noc_regions.csv")

# Group total medals won by NOC, removing duplicates from individuals winning medals from team sports to only count one medal
medals_country_df = athlete_events_df.dropna(subset=["Medal"])
medals_country_df = medals_country_df.drop_duplicates(subset=["NOC", "Games", "Year", "Season", "City", "Sport", "Event", "Medal"])
medals_country_df = medals_country_df.merge(noc_regions_df, on="NOC", how="left")
medals_country_df = medals_country_df.groupby(["region", "Medal"])["Medal"].count().unstack(fill_value=0).stack().reset_index(name="Medal Count")
medals_country_df = medals_country_df.groupby(["region"])["Medal Count"].sum().reset_index(name="Total Medals")

# Choropleth figure
choropleth_fig = px.choropleth(
    medals_country_df,
    title="Total Medals Won by Country",
    locations="region",
    locationmode="country names",
    hover_name="region",
    hover_data=dict(
        region=False
    ),
    color="Total Medals",
    range_color=[0, 500],
    color_continuous_scale="Viridis",
    projection="natural earth"
)

# Group total medals won by NOC, removing duplicates from individuals winning medals from team sports to only count one medal
medals_distribution_df = athlete_events_df.dropna(subset=["Medal"])
medals_distribution_df = medals_distribution_df.drop_duplicates(subset=["NOC", "Games", "Year", "Season", "City", "Sport", "Event", "Medal"])
medals_distribution_df = medals_distribution_df.merge(noc_regions_df, on="NOC", how="left")
medals_distribution_df = medals_distribution_df.groupby(["region", "Medal"])["Medal"].count().unstack(fill_value=0).stack().reset_index(name="Medal Count")

# List of medals won by NOC
noc_df_list = {col:noc for (col, noc) in medals_distribution_df.groupby("region")}

# Bar figure
medals_fig_list = {}
for key, noc in noc_df_list.items():
    medals_fig_list[key] = go.Figure(
        data=go.Bar(
            x=noc["Medal"],
            y=noc["Medal Count"]
        )
    )

choropleth_fig.update_layout(clickmode="event+select")

layout = html.Div([
    dcc.Graph(
        id="choropleth",
        figure=choropleth_fig
    ),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-text", children=[
            "Placeholder"
        ])),
        dcc.Graph(
            id="drill-in",
            figure=medals_fig_list["USA"]
        )],
        id="modal-sm",
        size="sm",
        is_open=False,
    ) 
])

@callback([
        Output("modal-text", "children"),
        Output("modal-sm", "is_open"),
        Output("drill-in", "figure")
    ],
    [Input("choropleth", "clickData")],
    [
        State("modal-sm", "is_open"),
        State("drill-in", "figure")
    ]
)
def update_modal(clickData, is_open, figure):
    if clickData is None:
        raise PreventUpdate
    if is_open is None:
        raise PreventUpdate
    if figure is None:
        raise PreventUpdate
        
    if clickData:
        return clickData["points"][0]["location"], not is_open, medals_fig_list[clickData["points"][0]["hovertext"]]
    return None, is_open, None