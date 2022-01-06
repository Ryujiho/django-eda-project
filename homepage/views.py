from django.shortcuts import render
import pandas as pd

from io import BytesIO
import os, base64
from pathlib import Path

from plotly.offline import plot
import plotly.graph_objects as go


    
BASE_DIR = Path(__file__).resolve().parent.parent
path_alcohol = os.path.join(BASE_DIR, 'homepage', 'static', 'alcohol.csv')
path_continents = os.path.join(BASE_DIR, 'homepage', 'static', 'continents.csv')

# Create Plots ---------------------------------------------------------
def make_graph_corr(alcohol_df):
    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    corr_df = alcohol_df.corr().apply(lambda x: round(x,2))

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Heatmap(df_to_plotly(corr_df),
                   hoverongaps = False, 
                    colorscale=[[0.0, '#B1D0E0'], 
                         [0.4, '#6998AB'],
                         [0.8, '#406882'], 
                         [1.0, '#1A374D']],
                    texttemplate="%{z}")
    )

    # Setting layout of the figure.
    layout = {
        'height': 400,
        'width': 450,
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div

def getNewDF(df_alcohol, df_continents):
    list = []
    for country in enumerate(df_alcohol.country.unique()):
        region = (df_continents[df_continents['name'] == country].region)
        if region.empty:
            list.append('NaN')
        else:
            list.append(str(region.item()))

    # Create continent column & Add new data to NaN fields.
    df_alcohol['continent'] = list
    df_alcohol.loc[df_alcohol.country == 'Korea, Rep.','continent']='Asia'
    df_alcohol.loc[df_alcohol.country == 'Swaziland','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Slovak Republic','continent']='Europe'
    df_alcohol.loc[df_alcohol.country == 'Yemen, Rep.','continent']='Asia'
    df_alcohol.loc[df_alcohol.country == 'Bosnia and Herzegovina','continent']='Europe'
    df_alcohol.loc[df_alcohol.country == 'Brunei','continent']='Asia'
    df_alcohol.loc[df_alcohol.country == 'Cape Verde','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Central African Rep.','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Congo, Dem. Rep.','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Congo, Rep.','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Cote d\'Ivoire','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Czech Rep.','continent']='Europe'
    df_alcohol.loc[df_alcohol.country == 'Dominican Rep','continent']='Americas'
    df_alcohol.loc[df_alcohol.country == 'Guinea-Bissau','continent']='Africa'
    df_alcohol.loc[df_alcohol.country == 'Macedonia, FYR','continent']='Europe'
    df_alcohol.loc[df_alcohol.country == 'Dominican Rep.','continent']='Africa'

    # Remove NaN
    df_alcohol.dropna(axis=0, inplace=True)

    # Group by Continent
    new_df = df_alcohol.groupby(by='continent').mean()
    return new_df

def make_graph_bar(alcohol_mean):
    graphs = []
    graphs.append(
        go.Bar(x=alcohol_mean.index.tolist(), y=alcohol_mean.alcconsumption.tolist(),
            name='Alcohol Consumption',
            marker_color='rgb(162, 205, 205)'
        ))
    graphs.append(
        go.Bar(x=alcohol_mean.index.tolist(), y=(alcohol_mean.incomeperperson/1000).tolist(),
            name='Income per person',
            marker_color='rgb(80, 32, 100)'
        ))
    graphs.append(
        go.Bar(x=alcohol_mean.index.tolist(), y=alcohol_mean.suicideper100th.tolist(),
            name='Suicide Per 100th',
            marker_color='rgb(213, 126, 126)'
        ))
    graphs.append(
        go.Bar(x=alcohol_mean.index.tolist(), y=(alcohol_mean.employrate/10).tolist(),
            name='Employ Rate',
            marker_color='rgb(255, 225, 175)'
        ))
    graphs.append(
        go.Bar(x=alcohol_mean.index.tolist(), y=(alcohol_mean.urbanrate/10).tolist(),
            name='Urban Rate',
            marker_color= 'rgb(198, 213, 126)'
        ))


    layout = {
        'height': 420,
        'width': 560,
    }

    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div

def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}

# Create your views here.-----------------------------------------------------
def index(request):
    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    df_mean_continent = getNewDF(df_alcohol, df_continents)

    # Send to HTML Template
    contents={}
    contents['csv_df'] = df_alcohol
    contents['plot_corr'] = make_graph_corr(df_alcohol)
    contents['plot_bar'] = make_graph_bar(df_mean_continent)

    return render(request, 'index.html', contents)

def step1(request):
    contents={}
    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    df_mean_continent = getNewDF(df_alcohol, df_continents)

    contents={}
    contents['csv_df'] = df_alcohol.head(5)
    contents['df_continents'] = df_continents.head(5)
    contents['df_mean_continent'] = df_mean_continent
    return render(request, 'step1.html', contents)

def step2(request):
    contents={}
    return render(request, 'step2.html', contents)


def step3(request):
    contents={}
    return render(request, 'step3.html', contents)


def tables(request):
    df_alcohol = pd.read_csv(path_alcohol)

    contents={}
    contents['csv_df'] = df_alcohol
    return render(request, 'tables.html', contents)


def charts(request):
    contents={}

    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    df_mean_continent = getNewDF(df_alcohol, df_continents)

    contents={}
    contents['plot_corr'] = make_graph_corr(df_alcohol)
    contents['plot_bar'] = make_graph_bar(df_mean_continent)
    return render(request, 'charts.html', contents)