import dash_core_components as dcc
import dash_html_components as html


def get_number_input(id, value=0, step=0.1, min=0):
    return dcc.Input(
        type="number", 
        id=id, 
        value=value, 
        step=step, 
        min=min,
        style={"margin": "10px", "width": "100%"},
    )
