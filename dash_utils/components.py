from dash import dcc


def get_number_input(id, value=0, step=0.001):
    return dcc.Input(
        type="number",
        id=id,
        value=value,
        step=step,
        style={"margin": "10px", "width": "100%"},
    )
