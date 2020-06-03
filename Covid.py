import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


deaths = pd.read_csv('/Users/alexandrubordei/Downloads/time_series_covid19_deaths_global.csv')
confirmed = pd.read_csv('/Users/alexandrubordei/Downloads/time_series_covid19_confirmed_global-2.csv')
recovered = pd.read_csv('/Users/alexandrubordei/Downloads/time_series_covid19_recovered_global.csv')


def total_sum():
    confirmed_case = confirmed['5/13/20'].sum()
    death_count = deaths['5/16/20'].sum()
    recovered_cases = recovered['5/17/20'].sum()
    print('total confirmed cases are: ' + str(confirmed_case))
    print('total deaths are: ' + str(death_count))
    print('total recovered cases are: ' + str(recovered_cases))

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
        new_df = new_df.append({'Country': country, 'Lat': Lat, 'Long': Long, 'Date': date, 'Confirmed': confirmed}, ignore_index=True)

    return new_df


def plot_dashly(confirmed):
    new_df = country_totals(confirmed)
    #confirmed.set_index('Country/Region')
    #grouped = confirmed.groupby('Country/Region')['5/13/20', 'Long', 'Lat'].apply(lambda g: g.nlargest(20).sum())
    #deaths.set_index('Country/Region')
    #confirmed['text'] = confirmed['5/13/20']+deaths['5/16/20']
    confirmed['text'] = confirmed['5/13/20']
    scale = 1000
    fig = go.Figure()


    for country in range(len(new_df)):
        fig.add_trace(go.Scattergeo(
            lon=new_df['Long'],
            lat=new_df['Lat'],
            text=new_df['Country'] + '<br>Confirmed ' + new_df['Confirmed'].astype(str),
            mode='markers',
            #+ new_df[],
            marker=dict(
                size=new_df['Confirmed'].astype(float)/scale,
                color='crimson',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
            ),
            #name=new_df['Country']
            #name='test'
        ))

        fig.update_layout(
            title_text='Cummulative Confirmed Cases',
            showlegend=False,
            geo=dict(
                scope='world',
                landcolor='rgb(217, 217, 217)',

            )
        )
    fig.show()

def plot_sums():
    index_confirmed = confirmed.set_index('Country/Region')
    confirmed_date_time = index_confirmed.iloc[:, 3:]
    summed_values = confirmed_date_time.sum(skipna=True)
    #print(summed_values)
    #summed_values.plot.line()
    #dash_graph = summed_values
    #plt.show()
    #return dash_graph

def plot_map():
    index_confirmed = confirmed.set_index('Country/Region')
    confirmed_date_time = index_confirmed.iloc[:, 3:]
    summed_values = confirmed_date_time.sum(skipna=True)
    fig = px.scatter_geo(summed_values, locations='Country/Region', color='continent',
                         hover_name='country', size='po',
                         projection="natural earth")
    fig.show()


if __name__ == '__main__':
    #total_sum(),
    #total_sum_by_region(),
    #plot_sums(),
    #plot_map(),
    plot_dashly(confirmed)
    #country_totals(raw_df = confirmed)
