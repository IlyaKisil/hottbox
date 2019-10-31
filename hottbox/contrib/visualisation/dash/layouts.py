"""
This module contains common layout components for dash apps
"""

import dash_core_components as dcc
import dash_html_components as html


def get_go_home_link():
    return dcc.Link('Go to Home', href='/home')


def get_home_layout():
    layout = html.Div([
        html.H3('Welcome to HOTTBOX GUI'),
        html.Div(
            dcc.Link('Go to App 1', href='/apps/app1'),
        ),
        html.Div(
            dcc.Link('Go to App 2', href='/apps/app2')
        ),
    ])
    return layout
