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
            href="/choropleth",
            # target="_blank"
        ),
        html.A(
            className="vis-card img-heatmap caption-heatmap",
            href="/heatmap",
            # target="_blank"
        ),
        html.A(
            className="vis-card img-sankey caption-sankey",
            href="/sankey",
            # target="_blank"
    )]),
    html.H4(["Greetings, enthusiasts of the Olympic spirit", html.Br(), """Welcome to an 
            immersive exploration into Olympic history. Dating back to the 1800’s, the 
            Olympic Games have allowed people spanning different generations and continents 
            to show off their athletic skills""", html.Br(), """ Our project, housed within a 
            Plotly Dashboard, serves as an interface in which you can explore Olympic data 
            through dynamic visualization. Within this Dashboard, users can interact with 
            three visualizations: A Global Map, A Heatmaps, and  A Sankey Diagram. Each 
            offers a unique lens through which to discover individual athlete performances, 
            country achievements, and contributing factors to Olympic success.""", html.Br(),
            """To aid exploration, we have crafted a series of user tasks designed to enhance
            the user experience:""", html.Br(), """Task 1: Users should see how trends differ 
            from decade to decade by filtering and aggregating data based on years or season.""",
            html.Br(), """Task 2: Users should be able to see individual countries’ Olympic 
            strengths and history by zooming in and clicking on particular countries.""", html.Br(),
            """Task 3: Users should be able to learn more about individual athletes’ journeys 
            and careers, as well as medal count, height, and weight through hover features.""", html.Br(),
            """Enjoy your charter through the course of Olympic history! Let the Games Begin!!!!"""])
])