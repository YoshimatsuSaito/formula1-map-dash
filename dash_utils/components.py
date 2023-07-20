from dash import dcc, html


def get_number_input(id, value=0, step=0.001, min=0):
    return dcc.Input(
        type="number", 
        id=id, 
        value=value, 
        step=step, 
        min=min,
        style={"margin": "10px", "width": "100%"},
    )
