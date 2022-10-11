from dash import dcc, html
from dash.dependencies import Input, Output, State

from viewflow.contrib.plotly import Dashboard, material
from . import options, utils
from .data import oildata


commont_graph_layout = {
    'autosize': True,
    'automargin': True,
    'margin': {'l': 30, 'r': 30, 'b': 20, 't': 40},
    'hovermode': 'closest',
    'plot_bgcolor': '#F9F9F9',
    'paper_bgcolor': '#F9F9F9',
    'legend': {'font': {'size': 10}, 'orientation': 'h'},
}


data_filter_layout = html.Div([
    html.Div([
        html.P(
            'Filter by construction date (or select range in histogram):',
            className="mdc-typography--subheading2 vf-form__formset-header",
        ),
        dcc.RangeSlider(
            id='year_slider',
            min=1960,
            max=2017,
            value=[2003, 2010],
        ),
        html.P(
            'Filter by well status:',
            className="mdc-typography--subheading2 vf-form__formset-header"
        ),
        dcc.RadioItems(
            id='well_status_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Active only ', 'value': 'active'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='active',
            labelStyle={'display': 'inline-block'},
            style={'padding-bottom': '20px'}
        ),
        dcc.Dropdown(
            id='well_statuses',
            options=options.well_status_options,
            multi=True,
            value=list(options.WELL_STATUSES.keys()),
            style={'margin-bottom': '20px'}
        ),
        html.P(
            'Filter by well type:',
            className="mdc-typography--subheading2 vf-form__formset-header"
        ),
        dcc.RadioItems(
            id='well_type_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Productive only ', 'value': 'productive'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='productive',
            labelStyle={'display': 'inline-block'},
            style={'padding-bottom': '8px'}
        ),
        dcc.Dropdown(
            id='well_types',
            options=options.well_type_options,
            multi=True,
            value=list(options.WELL_TYPES.keys()),
        ),
    ]),
])


cards_row_layout = material.InnerRow([
    material.Span3(
        material.Card(value_id="well_text", title="No. of Wells", color='#b80000')
    ),
    material.Span3(
        material.Card(value_id="gasText", title="Gas", icon='local_fire_department')
    ),
    material.Span3(
        material.Card(value_id="oilText", title="Oil", icon='local_gas_station')
    ),
    material.Span3(
        material.Card(value_id="waterText", title="Water", icon='water_damage')
    ),
], id="tripleContainer")


layout = material.PageGrid([
    dcc.Store(id='aggregate_data'),
    material.InnerRow([
        material.Span9([
            cards_row_layout,
            html.Div([
                dcc.Graph(id='count_graph',)
            ]),
        ]),
        material.Span3(data_filter_layout)
    ]),
    material.InnerRow([
        material.Span6([dcc.Graph(id='main_graph')]),
        material.Span6([dcc.Graph(id='individual_graph')]),
    ]),
    material.InnerRow([
        material.Span6([dcc.Graph(id='pie_graph')]),
        material.Span6([dcc.Graph(id='aggregate_graph')]),
    ]),
])


dashboard = Dashboard(
    app_name='oilngas',
    title='New York Oil and Gas',
    icon='local_gas_station',
    layout=layout
)


@dashboard.callback(
    Output('aggregate_data', 'data'),
    Input('well_statuses', 'value'),
    Input('well_types', 'value'),
    Input('year_slider', 'value'))
def update_production_text(well_statuses, well_types, year_slider):
    dff = utils.filter_dataframe(oildata.dataframe, well_statuses, well_types, year_slider)
    selected = dff['API_WellNo'].values
    index, gas, oil, water = utils.fetch_aggregate(oildata.points, selected, year_slider)
    return [utils.human_format(sum(gas)), utils.human_format(sum(oil)), utils.human_format(sum(water))]


@dashboard.callback(
    Output('well_statuses', 'value'),
    Input('well_status_selector', 'value'))
def display_status(selector):
    if selector == 'all':
        return list(options.WELL_STATUSES.keys())
    elif selector == 'active':
        return ['AC']
    else:
        return []


@dashboard.callback(
    Output('well_types', 'value'),
    Input('well_type_selector', 'value'))
def display_type(selector):
    if selector == 'all':
        return list(options.WELL_TYPES.keys())
    elif selector == 'productive':
        return ['GD', 'GE', 'GW', 'IG', 'IW', 'OD', 'OE', 'OW']
    else:
        return []


@dashboard.callback(
    Output('year_slider', 'value'),
    Input('count_graph', 'selectedData'))
def update_year_slider(count_graph_selected):
    if count_graph_selected is None:
        return [2003, 2010]
    else:
        values = []
        for point in count_graph_selected['points']:
            values.append(int(point['pointNumber']))

        return [min(values) + 1960, max(values) + 1961]


@dashboard.callback(
    Output('well_text', 'children'),
    Input('well_statuses', 'value'),
    Input('well_types', 'value'),
    Input('year_slider', 'value'))
def update_well_text(well_statuses, well_types, year_slider):
    dff = utils.filter_dataframe(oildata.dataframe, well_statuses, well_types, year_slider)
    return dff.shape[0]


@dashboard.callback(
    Output('gasText', 'children'),
    Input('aggregate_data', 'data'))
def update_gas_text(data):
    if data is not None:
        return data[0] + " mcf"
    return ''


@dashboard.callback(
    Output('oilText', 'children'),
    Input('aggregate_data', 'data'))
def update_oil_text(data):
    if data is not None:
        return data[1] + " bbl"
    return ''


@dashboard.callback(
    Output('waterText', 'children'),
    Input('aggregate_data', 'data'))
def update_water_text(data):
    if data is not None:
        return data[2] + " bbl"
    return ''


@dashboard.callback(
    Output('count_graph', 'figure'),
    Input('well_statuses', 'value'),
    Input('well_types', 'value'),
    Input('year_slider', 'value'))
def make_count_figure(well_statuses, well_types, year_slider):
    dff = utils.filter_dataframe(oildata.dataframe, well_statuses, well_types, [1960, 2017])
    g = dff[['API_WellNo', 'Date_Well_Completed']]
    g.index = g['Date_Well_Completed']
    g = g.resample('A').count()

    colors = []
    for i in range(1960, 2018):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append('rgb(123, 199, 255)')
        else:
            colors.append('rgba(123, 199, 255, 0.2)')

    return {
        'data': [
            {
                'type': 'scatter',
                'mode': 'markers',
                'x': g.index,
                'y': g['API_WellNo'] / 2,
                'name': 'All Wells',
                'opacity': 0,
                'hoverinfo': 'skip'
            },
            {
                'type': 'bar',
                'x': g.index,
                'y': g['API_WellNo'],
                'name': 'All Wells',
                'marker': {'color': colors}
            }
        ],
        'layout': {
            **commont_graph_layout,
            'title': 'Completed Wells/Year',
            'dragmode': 'select',
            'showlegend': False,
            'autosize': True,
        }
    }


@dashboard.callback(
    Output('main_graph', 'figure'),
    Input('well_statuses', 'value'),
    Input('well_types', 'value'),
    Input('year_slider', 'value'),
    State('main_graph', 'relayoutData'))
def make_main_figure(well_statuses, well_types, year_slider, main_graph_layout):

    dff = utils.filter_dataframe(oildata.dataframe, well_statuses, well_types, year_slider)

    mapbox_access_token = 'pk.eyJ1Ijoia21tYnZuciIsImEiOiJja3Vxc29haHUxbDhhMzFwMTJwdWVlbXcwIn0.UdKc0Y-tN0Fsc-SO9B5L3w'
    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

    graph_layout = {
        **commont_graph_layout,
        'title': 'Satellite Overview',
        'mapbox': {
            'accesstoken': mapbox_access_token,
            'style': 'light',
            'center': {'lon': -78.05, 'lat': 42.54},
            'zoom': 7,
        }
    }

    traces = []
    for well_type, dfff in dff.groupby('Well_Type'):
        trace = dict(
            type='scattermapbox',
            lon=dfff['Surface_Longitude'],
            lat=dfff['Surface_latitude'],
            text=dfff['Well_Name'],
            customdata=dfff['API_WellNo'],
            name=options.WELL_TYPES[well_type],
            marker=dict(size=4, opacity=0.6,)
        )
        traces.append(trace)

    if main_graph_layout is not None and 'mapbox.center' in main_graph_layout:
        lon = float(main_graph_layout['mapbox.center']['lon'])
        lat = float(main_graph_layout['mapbox.center']['lat'])
        zoom = float(main_graph_layout['mapbox.zoom'])
    else:
        lon = -78.05
        lat = 42.54
        zoom = 7

    graph_layout['mapbox']['center']['lon'] = lon
    graph_layout['mapbox']['center']['lat'] = lat
    graph_layout['mapbox']['zoom'] = zoom

    return {
        'data': traces,
        'layout': graph_layout
    }


@dashboard.callback(
    Output('individual_graph', 'figure'),
    Input('main_graph', 'hoverData'))
def make_individual_figure(main_graph_hover):
    if main_graph_hover is None:
        main_graph_hover = {
            'points': [
                {
                    'curveNumber': 4,
                    'pointNumber': 569,
                    'customdata': 31101173130000
                },
            ],
        }

    chosen = [point['customdata'] for point in main_graph_hover['points']]
    index, gas, oil, water = utils.fetch_individual(oildata.points, chosen[0])

    if index is None:
        return {
            'data': [],
            'layout': {
                **commont_graph_layout,
                'title': oildata.dataset[chosen[0]]['Well_Name'],
                'annotations': [{
                    'text': 'No data available',
                    'x': 0.5,
                    'y': 0.5,
                    'align': 'center',
                    'showarrow': False,
                    'xref': 'paper',
                    'yref': 'paper'
                }]
            }
        }

    gas_data = {
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Gas Produced (mcf)',
        'x': index,
        'y': gas,
        'line': {
            'shape': 'spline',
            'smoothing': 2,
            'width': 1,
            'color': '#fac1b7'
        },
        'marker': {'symbol': 'diamond-open'}
    }

    oil_data = {
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Oil Produced (bbl)',
        'x': index,
        'y': oil,
        'line': {
            'shape': 'spline',
            'smoothing': 2,
            'width': 1,
            'color': '#a9bb95'
        },
        'marker': {'symbol': 'diamond-open'}
    }

    water_data = {
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Water Produced (bbl)',
        'x': index,
        'y': water,
        'line': {
            'shape': 'spline',
            'smoothing': 2,
            'width': 1,
            'color': '#92d8d8'
        },
        'marker': {'symbol': 'diamond-open'}
    }

    return {
        'data': [gas_data, oil_data, water_data],
        'layout': {
            **commont_graph_layout,
            'title': oildata.dataset[chosen[0]]['Well_Name'],
        }
    }


@dashboard.callback(
    Output('aggregate_graph', 'figure'),
    Input('well_statuses', 'value'),
    Input('well_types', 'value'),
    Input('year_slider', 'value'),
    Input('main_graph', 'hoverData'))
def make_aggregate_figure(well_statuses, well_types, year_slider, main_graph_hover):
    if main_graph_hover is None:
        main_graph_hover = {
            'points': [{'curveNumber': 4, 'pointNumber': 569, 'customdata': 31101173130000}]
        }

    chosen = [point['customdata'] for point in main_graph_hover['points']]
    well_type = oildata.dataset[chosen[0]]['Well_Type']
    dff = utils.filter_dataframe(oildata.dataframe, well_statuses, well_types, year_slider)

    selected = dff[dff['Well_Type'] == well_type]['API_WellNo'].values
    index, gas, oil, water = utils.fetch_aggregate(oildata.points, selected, year_slider)

    gas_data = dict(
        type='scatter',
        mode='lines',
        name='Gas Produced (mcf)',
        x=index,
        y=gas,
        line=dict(
            shape="spline",
            smoothing="2",
            color='#F9ADA0'
        )
    )

    oil_data = dict(
        type='scatter',
        mode='lines',
        name='Oil Produced (bbl)',
        x=index,
        y=oil,
        line=dict(
            shape="spline",
            smoothing="2",
            color='#849E68'
        )
    )

    water_data = dict(
        type='scatter',
        mode='lines',
        name='Water Produced (bbl)',
        x=index,
        y=water,
        line=dict(
            shape="spline",
            smoothing="2",
            color='#59C3C3'
        )
    )

    return {
        'data': [gas_data, oil_data, water_data],
        'layout': {
            **commont_graph_layout,
            'title': 'Aggregate: ' + options.WELL_TYPES[well_type]
        }
    }


@dashboard.callback(
    Output('pie_graph', 'figure'),
    Input('well_statuses', 'value'),
    Input('well_types', 'value'),
    Input('year_slider', 'value'))
def make_pie_figure(well_statuses, well_types, year_slider):

    dff = utils.filter_dataframe(oildata.dataframe, well_statuses, well_types, year_slider)
    selected = dff['API_WellNo'].values
    index, gas, oil, water = utils.fetch_aggregate(oildata.points, selected, year_slider)
    aggregate = dff.groupby(['Well_Type']).count()

    data = [
        dict(
            type='pie',
            labels=['Gas', 'Oil', 'Water'],
            values=[sum(gas), sum(oil), sum(water)],
            name='Production Breakdown',
            text=['Total Gas Produced (mcf)', 'Total Oil Produced (bbl)',
                  'Total Water Produced (bbl)'],
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(
                colors=['#fac1b7', '#a9bb95', '#92d8d8']
            ),
            domain={"x": [0, .45], 'y':[0.2, 0.8]},
        ),
        dict(
            type='pie',
            labels=[options.WELL_TYPES[i] for i in aggregate.index],
            values=aggregate['API_WellNo'],
            name='Well Type Breakdown',
            hoverinfo="label+text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(
                colors=[options.WELL_COLORS[i] for i in aggregate.index]
            ),
            domain={"x": [0.55, 1], 'y':[0.2, 0.8]},
        )
    ]

    return {
        'data': data,
        'layout': {
            **commont_graph_layout,
            'title': 'Production Summary: {} to {}'.format(year_slider[0], year_slider[1]),
            'font': {'color': '#777777'},
            'legend': {
                'font': {'color': '#CCCCCC', 'size': '10'},
                'orientation': 'h',
                'bgcolor': 'rgba(0,0,0,0)'
            },
        }
    }
