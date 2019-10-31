import dash_core_components as dcc
import dash_html_components as html

from hottbox.contrib.visualisation.dash.layouts import get_go_home_link

layout = html.Div([
    html.H3('App 2 - TensorTKD Visualisation'),
    get_go_home_link(),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in ['NYC', 'MTL', 'LA']
        ]
    ),
    html.Div(id='app-2-display-value'),

])
