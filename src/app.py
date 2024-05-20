from dash import Dash, html, dcc, callback, Output, Input, State, page_container
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

import json
import os

from components import navbar

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        }
    ],
    suppress_callback_exceptions=True,
    title="Olympic Data Visualizations"
)

def serve_layout():
    return html.Div([
        navbar,
        dbc.Container(
            page_container,
            class_name="my-2 vis-container"
        )
    ])


app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=False)