from dash import Dash, html, dcc, callback, Output, Input, State, page_container
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import pandas as pd
import numpy as np

import json
import os
from dotenv import load_dotenv#, find_dotenv

from components import navbar

load_dotenv()
# uri = os.getenv("MONGODB_CONNECTION_STRING")
# client = MongoClient(uri, server_api=ServerApi('1'))

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
            class_name="my-2"
        )
    ])


app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=False)