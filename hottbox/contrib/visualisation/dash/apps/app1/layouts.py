import dash_core_components as dcc
import dash_html_components as html

from hottbox.contrib.visualisation.dash.layouts import get_go_home_link


layout = html.Div([
    html.H3('App 1 - TensorCPD Visualisation'),
    get_go_home_link(),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in ['NYC', 'MTL', 'LA']
        ]
    ),
    html.Div(id='app-1-display-value')
])
