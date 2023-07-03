import dash

from dash_utils.layout import get_layout
from dash_utils.data import create_data
from dash_utils.callbacks import register_callbacks, create_default_clickdata
from dash_utils.plotting import create_main_figure

SEASON = 2023
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap",
    "app.css",
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

data4app = create_data()
fig = create_main_figure(data4app.df, data4app.latest_gp_index, data4app.latest_gp_legend)
app.layout = get_layout(fig, SEASON)
default_clickdata = create_default_clickdata(data4app)
register_callbacks(app, data4app.df, data4app.latest_gp_index, default_clickdata)

if __name__ == "__main__":
    app.run_server(debug=True)
