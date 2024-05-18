from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Choropleth", href="/choropleth")),
        dbc.NavItem(dbc.NavLink("Heatmap", href="/heatmap")),
        dbc.NavItem(dbc.NavLink("Sankey", href="/sankey")),
        dbc.NavItem(dbc.NavLink("Axis Banking", href="/bank")),
    ],
    brand="Olympic Data Visualizations",
    brand_href="/",
    color="primary",
    dark=True,
)