from dash.dependencies import Input, Output

from hottbox.contrib.visualisation.dash.app import app


@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You wish you had selected "{}"'.format(value)
