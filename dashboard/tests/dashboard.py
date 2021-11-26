from dash import dcc, html
from dash.dependencies import Input, Output

from viewflow.contrib.plotly import Dashboard, material

dashboard = Dashboard(
    title='Test dashboard',
    layout=material.PageGrid([
        material.InnerRow([
            material.Span12([
                dcc.RadioItems(
                    id='dropdown-color',
                    options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
                    value='red'
                ),
                html.Div(id='output-color'),
                dcc.RadioItems(
                    id='dropdown-size',
                    options=[{'label': i, 'value': j} for i, j in [('L', 'large'), ('M', 'medium'), ('S', 'small')]],
                    value='medium'
                ),
                html.Div(id='output-size'),
            ])
        ])
    ])
)


@dashboard.callback(
    Output('output-color', 'children'),
    [Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value


@dashboard.callback(
    Output('output-size', 'children'),
    [Input('dropdown-color', 'value'),
     Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." % (dropdown_size, dropdown_color)
