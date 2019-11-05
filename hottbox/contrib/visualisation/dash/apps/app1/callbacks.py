import codecs
import pickle

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


from hottbox.contrib.visualisation.dash.app import app
from hottbox.contrib.visualisation.dash.utils import DynamicComponentsID, generate_dropdown_options

# This is for type hints
from hottbox.core import TensorCPD


DYNAMIC_ELEMENTS = {
    "dropdown-select-component": 1,
    "input-title": 10,
    "graph": 10,
}
MAX_NUMBER_OF_FIGURES = max(DYNAMIC_ELEMENTS.values())
ID_LOOKUP = DynamicComponentsID(
    elements=DYNAMIC_ELEMENTS
)


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
    for i, mode_name in enumerate(tensor_unpickle.mode_names):
        graphs.append(
            dcc.Graph(
                id=ID_LOOKUP.get_by_number(prefix="graph", number=i),
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
        id=ID_LOOKUP.get_by_number(prefix="dropdown-select-component"),
        options=generate_dropdown_options(options_list=range(number_of_components)),
        placeholder="Select component to display ..."
    )
    input_list = []
    for i, mode_name in enumerate(tensor.mode_names):
        input_div = dcc.Input(
            id=ID_LOOKUP.get_by_number(prefix="input-title", number=i),
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


def _create_figure(title=None, selected_component=None, data_string=None, id=None):
    figure = {
        'layout': _create_figure_layout(title=f"{title}<br>(Selected component {selected_component})"),
    }
    if selected_component is not None:

        # This is a hacky way to determine which figure should be update
        # since, we can't use the same dash element for input and output
        # within the same callback
        mode = ID_LOOKUP.get_by_id(prefix="input-title", id=id)

        tensor_unpickle: TensorCPD = _convert_to_tensor(data_string)
        figure['data'] = _create_figure_trace(
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


def _create_figure_trace(x, y, type_):
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


for fig_number in range(MAX_NUMBER_OF_FIGURES):
    dropdown_id = ID_LOOKUP.get_by_number(prefix="dropdown-select-component")
    graph_id = ID_LOOKUP.get_by_number(prefix="graph", number=fig_number)
    title_id = ID_LOOKUP.get_by_number(prefix="input-title", number=fig_number)
    app.callback(
        output=Output(graph_id, 'figure'),
        inputs=[
            Input(title_id, 'value'),
            Input(dropdown_id, 'value')
        ],
        state=[
            State('app-1-placeholder-tensor-cpd', 'children'),  # TODO: probably should be an input
            State(title_id, 'id')
        ]
    )(_create_figure)
