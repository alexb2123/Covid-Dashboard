import dash
import dash_core_components as dcc
import dash_html_components as html
import Covid
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash()

fig = go.Figure(Covid.plot_bubble_map(Covid.confirmed, Covid.deaths, Covid.recovered))

colors = {
    'background': '#FFFFFF',
    'text': '#000000',
}

confirmed_cases = Covid.confirmed
death_cases = Covid.deaths
recovered_cases = Covid.recovered


opts = [{'label': 'Confirmed Cases', 'value': 'confirmed_cases'},
        {'label': 'Death Cases', 'value': 'death_cases'},
        {'label': 'Recovered Cases', 'value': 'recovered_cases'}]

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    #header
    html.H1(
        children='Global Coronavirus Incidence',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    #titles
    html.Div(children='Coronavirus 2020', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    #map
    dcc.Graph(
        id='bubble_map',
        figure=fig
    ),

    #dropdown
    #html.P([
    #    html.Label("Choose your dataset", style={'padding-left': '100px'}),
    #    dcc.Dropdown(id='opt', options=opts,
    #                 )
    #        ], style={'width': '500px',
    #                  'fontSize': '20px',
    #                  'padding-left': '100px',
    #                  'display': 'inline-block'}),
    #
    #
#    #slider
#    html.P([
#        html.Label('Dates'),
#        dcc.RangeSlider(id('slider',
#                           ))
#    ])

])


#-----------------------------------------------------------------

#@app.callback(
#    Output(component_id='bubble_map', component_property='figure'),
#    [Input(component_id='opt', component_property='value')]
#)
#
#def update_graph(input_value):
#    df_confirmed = Covid.confirmed
#    df_recovered = Covid.recovered
#    df_deaths = Covid.deaths
#
#    def check_input():
#        if Input.component_property == confirmed_cases:
#            dff = df_confirmed
#        elif Input.component_property == recovered_cases:
#            dff = df_recovered
#        else:
#            dff = df_deaths
#
#        return dff




if __name__ == '__main__':
    app.run_server(debug=True)
