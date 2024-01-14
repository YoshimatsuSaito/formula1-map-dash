import datetime

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from dash_utils.callbacks import (register_page1_callbacks,
                                  register_page2_callbacks)
from dash_utils.data import create_data
from dash_utils.index import register_index_callback
from dash_utils.plotting import create_main_figure
from modules.predictor import get_df_prediction

# Set information
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap",
    "app.css",
    dbc.themes.BOOTSTRAP,
]
SEASON = datetime.datetime.now().year
try:
    data4app = create_data(SEASON)
except ValueError:
    SEASON -= 1
    data4app = create_data(SEASON)
df_prediction = get_df_prediction()
df_prediction = df_prediction.loc[df_prediction["year"] == SEASON]
fig = create_main_figure(
    data4app.df, data4app.latest_gp_index, data4app.latest_gp_legend
)

# Create an app
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ]
)
server = app.server

# Register callback
register_index_callback(app, fig, SEASON, df_prediction)
register_page1_callbacks(app, data4app)
register_page2_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server()
