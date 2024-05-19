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
    path="/bank",
    title="Bank"
)

MIN_YEAR = 1994
MAX_YEAR = 2016


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

#only select USA and China data from years 1994 - 2016 for demonstration purposes
regions_of_interest = ["USA", "China"]
filtered_success_rate_df = success_rate_df[success_rate_df['region'].isin(regions_of_interest) & (success_rate_df['Year'].between(MIN_YEAR, MAX_YEAR))]

#og plot
bank_fig = px.line(filtered_success_rate_df, x="Year", y="Success Rate", color='region', title='Success Rate Over Years (Original)',
        width=600, height=600)

#line of best fit for usa
usa_data = filtered_success_rate_df[filtered_success_rate_df['region'] == 'USA']
fit = np.polyfit(usa_data['Year'], usa_data['Success Rate'], 1)
fit_fn = np.poly1d(fit)

# Plot before and after figures
bank_fig_after = px.line(filtered_success_rate_df, x="Year", y="Success Rate", color='region', title='Success Rate Over Years (After Scaling)',
        width=600, height=600)
bank_fig_after.add_scatter(x=usa_data['Year'], y=fit_fn(usa_data['Year']), mode='lines', name='USA Trendline')

# Adjust y-axis to make the trendline have a slope of 45 degrees
y_min = fit_fn(MIN_YEAR-6)
y_max = fit_fn(MAX_YEAR+6)
bank_fig_after.update_yaxes(range=[y_min, y_max])

# Add equivalent padding to the x-axis
bank_fig_after.update_xaxes(range=[MIN_YEAR-6, MAX_YEAR+6])

layout = html.Div([
    html.H1("""USA vs China: How Do They Compare in Modern Day Olympic Success?"""),
    html.Div([
        dcc.Graph(
            id="bank",
            figure=bank_fig, 
            style={'display': 'inline-block', 'width': '49%'}
        ),
        dcc.Graph(
            id="bank2",
            figure=bank_fig_after, 
            style={'display': 'inline-block', 'width': '49%'},
        ),
    ]),
    html.P("""Before and after results of applying automatic axis scaling to USA and China's recent olympic success story. Good for comparisons between two of the biggest powerhouses in the world.""")
])