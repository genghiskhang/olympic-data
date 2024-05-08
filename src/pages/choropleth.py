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

# Choropleth figure
choropleth_fig = px.choropleth(
    success_rate_df,
    animation_frame='Year',
    animation_group='Success Rate',
    title="Success Rate for Medals Won by Country",
    locations="region",
    locationmode="country names",
    hover_name="region",
    hover_data=dict(
        region=False,
        Year=False
    ),
    color="Success Rate",
    color_continuous_scale="BuGn",
    projection="natural earth"
)
choropleth_fig["layout"].pop("updatemenus")
choropleth_fig.update_layout(
    margin=dict(l=80, r=80, t=60, b=60),
    width=800,
    height=600
)

# Group total medals won by NOC, removing duplicates from individuals winning medals from team sports to only count one medal
medals_distribution_df = athlete_events_df.dropna(subset=["Medal"])
medals_distribution_df = medals_distribution_df.drop_duplicates(subset=["NOC", "Games", "Year", "Season", "City", "Sport", "Event", "Medal"])
medals_distribution_df = medals_distribution_df.merge(noc_regions_df, on="NOC", how="left")
medals_distribution_df = medals_distribution_df.groupby(["Year", "region", "Medal"])["Medal"].count().unstack(fill_value=0).stack().reset_index(name="Medal Count")

color_seq = ["#CD7F32", "#C0C0C0", "#D4AF37"]

# List of medals won by NOC
year_df_list = {col:year for (col, year) in medals_distribution_df.groupby("Year")}

# Bar figure
medals_fig_list = {}
for year, df in year_df_list.items():
    for (country, row) in df.groupby('region'):
        if year not in medals_fig_list:
            medals_fig_list[year] = {}
        medals_fig_list[year][country] = go.Figure(
            data=go.Bar(
                x=row["Medal"],
                y=row["Medal Count"],
            )
        )
        medals_fig_list[year][country].update_layout(
            title=f"{country} in {year}",
            xaxis={'categoryorder':'array', 'categoryarray':["Bronze", "Silver", "Gold"]}
        )

choropleth_fig.update_layout(clickmode="event+select")

layout = html.Div(id="choropleth-container", children=[
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
            figure=go.Figure()
        ),
        html.P("A bar chart displaying the distribution of medals won by each individual country."),
    ],
    id="modal-sm",
    size="sm",
    is_open=False,
    ),
    html.P("""A choropleth figure displaying the proportion of total medals won across all 
               countries out of total medals attempted. Hovering over a specific country will 
               display the olympic success rate for that country."""),
])

@callback([
        Output("modal-text", "children"),
        Output("modal-sm", "is_open"),
        Output("drill-in", "figure")
    ],
    [
        Input("choropleth", "clickData"),
        Input("choropleth", "figure")
    ],
    [
        State("modal-sm", "is_open"),
        State("drill-in", "figure")
    ]
)
def update_modal(clickData, cho_fig, is_open, figure):
    if clickData is None:
        raise PreventUpdate
    if cho_fig is None:
        raise PreventUpdate
    if is_open is None:
        raise PreventUpdate
    if figure is None:
        raise PreventUpdate
        
    if clickData:
        return clickData["points"][0]["hovertext"], not is_open, medals_fig_list[int(cho_fig['layout']['sliders'][0]['steps'][cho_fig['layout']['sliders'][0]['active']]['label'])][clickData["points"][0]["hovertext"]]
    return None, is_open, None