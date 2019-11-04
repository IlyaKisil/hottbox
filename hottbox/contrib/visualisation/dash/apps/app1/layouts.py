import dash_core_components as dcc
import dash_html_components as html

from hottbox.contrib.visualisation.dash.layouts import get_go_home_link
from hottbox.contrib.visualisation.dash.style import DISPLAY_NONE


layout = html.Div([
    html.H3('App 1 - TensorCPD Visualisation'),
    get_go_home_link(),
    dcc.Upload(
        id="upload",
        children=[
            'Drag and Drop or ',
            html.A('Select a File')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }
    ),
    html.Div(id='app-1-placeholder-tensor-cpd', style=DISPLAY_NONE),
    html.Div(id='app-1-tensor-cpd-meta', style=DISPLAY_NONE),
    # html.Div(id='app-1-tensor-cpd-meta'),
    html.Div(id='app-1-visualisation-controls-container'),
    html.Div(id='app-1-tensor-cpd-plots-container'),
    html.Div(id='app-1-dropdown-output-container'),
])
