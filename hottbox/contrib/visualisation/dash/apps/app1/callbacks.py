import codecs
import pickle

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


from hottbox.contrib.visualisation.dash.app import app

# FIXME: get rid of start import
from hottbox.contrib.visualisation.dash.utils import *

# This is type hints
from hottbox.core import TensorCPD


# TODO: need to generate a lookup table for ids of elements.

def _convert_to_tensor(data_string):
    data = data_string.encode("utf8").split(b";base64,")[1]

    tensor_unpickle = pickle.loads(codecs.decode(data, "base64"))
    return tensor_unpickle


@app.callback(
    Output('app-1-placeholder-tensor-cpd', 'children'),
    [
        Input('upload', 'contents')
    ]
)
def read_tensor_file(contents):
    if not contents:
        raise PreventUpdate

    return contents

@app.callback(
    Output('app-1-tensor-cpd-meta', 'children'),
    [
        Input('app-1-placeholder-tensor-cpd', 'children')
    ]
)
def display_tensorcpd_meta(data):
    if not data:
        raise PreventUpdate

    tensor_unpickle = _convert_to_tensor(data)

    out = \
        f"""
        Number of elements: {tensor_unpickle.ft_shape}
        Rank: {tensor_unpickle.rank}
        Number of plots required: {tensor_unpickle.order}
        Plot names: {tensor_unpickle.mode_names}
        """
    return out


@app.callback(
    Output('app-1-visualisation-controls-container', 'children'),
    [
        Input('app-1-placeholder-tensor-cpd', 'children')
    ]
)
def create_tensor_visualisation(data):
    if not data:
        raise PreventUpdate

    tensor_unpickle: TensorCPD = _convert_to_tensor(data)
    elements = _create_vis_controls(tensor_unpickle)

    graphs = []
    for mode_name in tensor_unpickle.mode_names:
        graphs.append(
            dcc.Graph(
                id=generate_plot_id(mode_name=mode_name),
                figure=_create_figure(
                    data_string=data,
                    title=mode_name
                )
            )
        )

    div = html.Div(
        children=[
            dbc.Row([
                dbc.Col(elements["dropdown"]),
            ]),
            dbc.Row([
                dbc.Col(children=html.Div([e, graphs[i]]), style={"border": "2px solid"}) for i, e in enumerate(elements["input-list"])
            ])
        ]
    )

    return div


def _create_vis_controls(tensor):
    number_of_components = tensor.rank[0]
    dropdown = dcc.Dropdown(
        id=generate_component_dropdown_id("generic"),
        options=generate_dropdown_options(options_list=range(number_of_components)),
        placeholder="Select component to display ..."
    )
    input_list = []
    for i, mode_name in enumerate(tensor.mode_names):
        input_div = dcc.Input(
            id=generate_title_input_id(mode_name=mode_name),
            type="text",
            persistence=True,
            persistence_type="memory",
            value=mode_name,
            style={"width": "100%"},
            placeholder=f"Title for component plot {i} ..."
        )
        input_list.append(input_div)

    controls = {
        "dropdown": dropdown,
        "input-list": input_list
    }
    return controls


def _create_figure(title=None, selected_component=None, data_string=None, bla=None):
    figure = {
        'layout': _create_figure_layout(title=f"Selected component: {selected_component} (for {title})"),

    }
    if selected_component is not None:

        mode = int(bla.split("-")[-1])  # Reverse engineer, for which mode we create a figure

        tensor_unpickle: TensorCPD = _convert_to_tensor(data_string)
        figure['data'] = _create_figure_data(
            y=tensor_unpickle.fmat[mode][:, selected_component],
            x=[j for j in range(tensor_unpickle.ft_shape[mode])],
            type_='bar'
        )

    return figure

def _create_figure_layout(title):
    layout = {
        'clickmode': 'event+select',
        'title': title,
        'xaxis': {
            'title': "Component feature number"
        },
        'yaxis': {
            'title': "Component feature value"
        },

    }
    return layout

def _create_figure_data(x, y, type_):
    if type_ == "line":
        data = [
            go.Scatter(
                x=x,
                y=y,
                mode='lines'
            )
        ]
    else:
        data = [
            go.Bar(
                x=x,
                y=y,
            )
        ]
    return data

for mode_name in ["mode-0", "mode-1", "mode-2"]:
    app.callback(
        output=Output(generate_plot_id(mode_name=mode_name), 'figure'),
        inputs=[
            Input(generate_title_input_id(mode_name=mode_name), 'value'),
            Input(generate_component_dropdown_id("generic"), 'value')
        ],
        state=[
            State('app-1-placeholder-tensor-cpd', 'children'),  # TODO: probably should be an input
            State(generate_title_input_id(mode_name=mode_name), 'id')
        ]
    )(_create_figure)
