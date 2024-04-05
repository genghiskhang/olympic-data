from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],
    # use_pages=True
)

df = pd.read_csv("aid_data.csv")
df = df.dropna()

# Dataframe for sum of donations given grouped by country
donors_df = df.rename(columns={"donor":"country"}).sort_values(by=["commitment_amount_usd_constant"], ascending=True).groupby(["country"])["commitment_amount_usd_constant"].sum().reset_index(name="total_donated")

# Dataframe for sum of donations received grouped by country
recipients_df = df.rename(columns={"recipient":"country"}).groupby(["country"])["commitment_amount_usd_constant"].sum().reset_index(name="total_received")

# Dataframe for net donations grouped by country
combined_df = pd.merge(donors_df, recipients_df, how="outer", on="country").fillna(0)
combined_df["net"] = combined_df["total_donated"] - combined_df["total_received"]

# Choropleth figure
fig_q1 = px.choropleth(combined_df,
                        title="Net Donations by Country",
                        locations="country",
                        locationmode="country names",
                        color="net",
                        color_continuous_scale="PiYg",
                        hover_name="country",
                        range_color=[-4e6, 4e6],
                        projection="natural earth")

fig_q1.update_layout(clickmode='event+select')

country = None

app.layout = html.Div([
    dcc.Graph(
        id="test-map",
        figure=fig_q1
    ),
    # html.H1(id='hover-data', children=[
    #     "Test Header"
    # ]),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(id="modal-text", children=[
                "Placeholder"
            ]))
        ],
        id="modal-sm",
        size="sm",
        is_open=False,
    )
])

# @callback(
#     Output('hover-data', 'children'),
#     Input('test-map', 'clickData')
# )
# def display_click_data(clickData):
#     # return json.dumps(clickData, indent=2)["points"][0]
#     if clickData:
#         country = clickData["points"][0]["location"]
#         return clickData["points"][0]["location"]
#     country = None
#     return None

@callback([
        Output("modal-text", "children"),
        Output("modal-sm", "is_open")
    ],[
        Input("test-map", "clickData")
    ],[
        State("modal-sm", "is_open")
    ]
)
def update_modal(clickData, is_open):
    # print(clickData)
    if clickData:
        return clickData["points"][0]["location"], not is_open
    return None, is_open
    # return clickData

# def toggle_modal(n1, is_open):
#     if n1:
#         print(is_open)
#         return not is_open
#     print(is_open)
#     return is_open

# app.callback(
#     Output("modal-sm", "is_open"),
#     Input("open-sm", "n_clicks"),
#     State("modal-sm", "is_open"),
# )(toggle_modal)

if __name__ == "__main__":
    app.run(debug=True)