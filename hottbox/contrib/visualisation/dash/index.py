import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from hottbox.contrib.visualisation.dash.app import app
from hottbox.contrib.visualisation.dash.apps import app1, app2
from hottbox.contrib.visualisation.dash.layouts import get_home_layout


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return get_home_layout()
