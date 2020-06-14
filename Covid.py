import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
#import DashBoard


deaths = pd.read_csv('/Users/alexandrubordei/Downloads/time_series_covid19_deaths_global.csv')
confirmed = pd.read_csv('/Users/alexandrubordei/Downloads/time_series_covid19_confirmed_global-2.csv')
recovered = pd.read_csv('/Users/alexandrubordei/Downloads/time_series_covid19_recovered_global.csv')


#names
names = {'deaths': 'deaths', 'confirmed': 'confirmed', 'recovered': 'recovered'}



#total global conirmed, dead, and recovered
def total_sum():
    confirmed_case = confirmed['5/13/20'].sum()
    death_count = deaths['5/16/20'].sum()
    recovered_cases = recovered['5/17/20'].sum()
    print('total confirmed cases are: ' + str(confirmed_case))
    print('total deaths are: ' + str(death_count))
    print('total recovered cases are: ' + str(recovered_cases))


#total sums by country using lambdas
def total_sum_by_region():
    confirmed.set_index('Country/Region')
    data = confirmed.groupby('Country/Region')['5/13/20'].apply(lambda g: g.nlargest(20).sum())
    data2 = data.sort_values(ascending=False)
    print(data2)

    deaths.set_index('Country/Region')
    data = deaths.groupby('Country/Region')['5/16/20'].apply(lambda g: g.nlargest(20).sum())
    data2 = data.sort_values(ascending=False)
    print(data2)

    recovered.set_index('Country/Region')
    data = recovered.groupby('Country/Region')['5/17/20'].apply(lambda g: g.nlargest(20).sum())
    data2 = data.sort_values(ascending=False)
    print(data2)

#bilals method of creating a new df
def country_totals(raw_df):
    #print(raw_df['Country/Region'].unique())
    #print(raw_df.columns)
    #print(raw_df[raw_df['Country/Region'] == 'China'][['5/']])
    new_df = pd.DataFrame(columns=('Country', 'Lat', 'Long', 'Date', 'Confirmed'))

    for country in raw_df['Country/Region'].unique():
    #    print(country, raw_df[raw_df['Country/Region'] == country]['5/13/20'].sum())
        date = '5/13/20'
        confirmed = raw_df[raw_df['Country/Region'] == country][date].sum()
        Lat = raw_df[raw_df['Country/Region'] == country]['Lat'].mean()
        Long = raw_df[raw_df['Country/Region'] == country]['Long'].mean()
        new_df = new_df.append({'Country': country, 'Lat': Lat, 'Long': Long, 'Date': date, 'Confirmed': confirmed},
                               ignore_index=True)

    return new_df

#----------------------------------------------------------------------------------------------------------

#plotting a plotly map
def plot_bubble_map(confirmed_data_frame, death_data_frame, recovered_data_frame):
    confirmed_data_frame['text'] = confirmed_data_frame['5/13/20']
    scale = 600
    fig = go.Figure()

#loop confirmed
    for country in range(len(confirmed_data_frame)):
        fig.add_trace(go.Scattergeo(
            lon=confirmed_data_frame['Long'],
            lat=confirmed_data_frame['Lat'],
            text=confirmed_data_frame['Country/Region'] + '<br>{} '.format(names.get('confirmed')) + confirmed_data_frame['5/13/20'].astype(str),
            mode='markers',
            marker=dict(
                size=confirmed_data_frame['5/13/20'].astype(float)/scale,
                color='yellow',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
            ),
            name=''
        )),

#loop death
    for country in range(len(death_data_frame)):
        fig.add_trace(go.Scattergeo(
            lon=death_data_frame['Long'],
            lat=death_data_frame['Lat'],
            text=death_data_frame['Country/Region'] + '<br>{} '.format(names.get('deaths')) + death_data_frame['5/13/20'].astype(str),
            mode='markers',
            marker=dict(
                size=death_data_frame['5/13/20'].astype(float)/scale,
                color='crimson',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
            ),
            name=''
        )),

#loop recovered
    for country in range(len(recovered_data_frame)):
        fig.add_trace(go.Scattergeo(
            lon=recovered_data_frame['Long'],
            lat=recovered_data_frame['Lat'],
            text=recovered_data_frame['Country/Region'] + '<br>{} '.format(names.get('recovered')) + recovered_data_frame['5/13/20'].astype(str),
            mode='markers',
            marker=dict(
                size=recovered_data_frame['5/13/20'].astype(float)/scale,
                color='green',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
            ),
            name=''
        )),

    fig.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                active=0,
                showactive=True,
                buttons=[{'label': 'Confirmed',
                     'method': 'update',
                          'args': [{'visible': [True, False, False]},
                                   {'title': 'Confirmed Cases'}]},
                        {'label': 'Deaths',
                         'method': 'update',
                         'args': [{'visible': [False, True, False]},
                                  {'title': 'Recovered Cases'}]},
                        {'label': 'Recovered',
                         'method': 'update',
                         'args': [{'visible': [False, False, True]},
                                  {'title': 'Deaths'}]},
                         ]),
        ],
        #title_text='',
        showlegend=False,
        overwrite=True,
        geo=dict(
            scope='world',
            landcolor='rgb(217, 217, 217)'))

    return fig
    #fig.show()

#----------------------------------------------------------------------------------------------------------

#pandas plot confirmed
def plot_sums():
    index_confirmed = confirmed.set_index('Country/Region')
    confirmed_date_time = index_confirmed.iloc[:, 3:]
    summed_values = confirmed_date_time.sum(skipna=True)
    #print(summed_values)
    summed_values.plot.line()
    #dash_graph = summed_values
    plt.show()
    #return dash_graph



if __name__ == '__main__':
    #total_sum(),
    #total_sum_by_region(),
    #plot_sums(),
    #plot_map(),
    plot_bubble_map(confirmed, deaths, recovered)
    #country_totals(raw_df = confirmed)
    #name_game(plot_dashly())
    #update_layouts()
