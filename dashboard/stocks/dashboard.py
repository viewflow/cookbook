import dash
from dash import dcc, html

import colorlover as cl

from viewflow.contrib.plotly import Dashboard, material
from .data import stockData

colorscale = cl.scales['9']['qual']['Paired']


layout = material.PageGrid([
    material.InnerRow([
        material.Span12([
            dcc.Dropdown(
                id='stock-ticker-input',
                options=[
                    {'label': s[0], 'value': str(s[1])}
                    for s in zip(stockData.dataframe.Stock.unique(), stockData.dataframe.Stock.unique())
                ],
                value=['YHOO', 'GOOGL'],
                multi=True
            ),
        ]),
        material.Span12([
            html.Div(id='graphs')
        ]),
    ])
])


dashboard = Dashboard(
    app_name='stocks',
    title='Finance Explorer',
    icon='timeline',
    layout=layout
)


def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band


@dashboard.callback(
    dash.dependencies.Output('graphs', 'children'),
    dash.dependencies.Input('stock-ticker-input', 'value')
)
def update_graph(tickers):
    graphs = []

    if not tickers:
        graphs.append(html.H3(
            "Select a stock ticker.",
            style={'marginTop': 20, 'marginBottom': 20}
        ))
    else:
        for i, ticker in enumerate(tickers):

            dff = stockData.dataframe[stockData.dataframe['Stock'] == ticker]

            candlestick = {
                'x': dff['Date'],
                'open': dff['Open'],
                'high': dff['High'],
                'low': dff['Low'],
                'close': dff['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(dff.Close)
            bollinger_traces = [{
                'x': dff['Date'], 'y': y,
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i * 2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(
                material.InnerRow([
                    material.Span12([
                        html.Div([
                            dcc.Graph(
                                id=ticker,
                                figure={
                                    'data': [candlestick] + bollinger_traces,
                                    'layout': {
                                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                                        'legend': {'x': 0}
                                    }
                                }
                            ),
                        ], className="mdc-card mdc-card--outlined")
                    ])
                ])
            )

    return graphs
