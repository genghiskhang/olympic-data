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
    path="/",
    redirect_from=["/home"],
    title="Home"
)

layout = html.Div([
    html.Div([
        html.A(
            className="vis-card img-choropleth caption-choropleth",
            href="/choropleth"
        ),
        html.A(
            className="vis-card img-heatmap caption-heatmap",
            href="/heatmap"
        ),
        html.A(
            className="vis-card img-sankey caption-sankey",
            href="/sankey"
    )])
])