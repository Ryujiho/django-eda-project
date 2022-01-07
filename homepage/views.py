from django.shortcuts import render
import pandas as pd

from io import BytesIO
import os, base64
from pathlib import Path

from plotly.offline import plot
import plotly.graph_objects as go


# global variables (csv)
BASE_DIR = Path(__file__).resolve().parent.parent
path_alcohol = os.path.join(BASE_DIR, 'homepage', 'static', 'alcohol.csv')
path_continents = os.path.join(BASE_DIR, 'homepage', 'static', 'continents.csv')
df_alcohol = pd.read_csv(path_alcohol)
df_continents = pd.read_csv(path_continents)


# Create Plots ---------------------------------------------------------
def make_graph_corr(df):
    corr_df = df.corr().apply(lambda x: round(x,2))
    columns_name = ['Alcohol Consumption','Income per person','Suicide Per 100th','Employ Rate','Urban Rate']

    graphs = []
    graphs.append(
        go.Heatmap(
                    {'z': corr_df.values.tolist(),
                    'x': columns_name,
                    'y': columns_name},
                   hoverongaps = False, 
                    colorscale=[[0.0, '#B1D0E0'], 
                         [0.4, '#6998AB'],
                         [0.8, '#406882'], 
                         [1.0, '#1A374D']],
                    texttemplate="%{z}")
    )
    layout = {
        'title': '<b>컬럼별 상관계수 비교</b> <br><sup>색이 진할수록 높은 상관계수를 가진다.</sup>',
        'height': 400,
        'width': 450,
    }

    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div

def getNewDF(df, df_continents):
    list = []
    for idx, country in enumerate(df.country.unique()):
        region = (df_continents[df_continents['name'] == country].region)
        if region.empty:
            list.append('NaN')
        else:
            list.append(str(region.item()))

    # Create continent column & Add new data to NaN fields.
    df['continent'] = list
    df.loc[df.country == 'Korea, Rep.','continent']='Asia'
    df.loc[df.country == 'Swaziland','continent']='Africa'
    df.loc[df.country == 'Slovak Republic','continent']='Europe'
    df.loc[df.country == 'Yemen, Rep.','continent']='Asia'
    df.loc[df.country == 'Bosnia and Herzegovina','continent']='Europe'
    df.loc[df.country == 'Brunei','continent']='Asia'
    df.loc[df.country == 'Cape Verde','continent']='Africa'
    df.loc[df.country == 'Central African Rep.','continent']='Africa'
    df.loc[df.country == 'Congo, Dem. Rep.','continent']='Africa'
    df.loc[df.country == 'Congo, Rep.','continent']='Africa'
    df.loc[df.country == 'Cote d\'Ivoire','continent']='Africa'
    df.loc[df.country == 'Czech Rep.','continent']='Europe'
    df.loc[df.country == 'Dominican Rep','continent']='Americas'
    df.loc[df.country == 'Guinea-Bissau','continent']='Africa'
    df.loc[df.country == 'Macedonia, FYR','continent']='Europe'
    df.loc[df.country == 'Dominican Rep.','continent']='Africa'

    df.loc[df.country == 'Faeroe Islands','continent']='Europe'
    df.loc[df.country == 'Hong Kong, China','continent']='Asia'
    df.loc[df.country == 'Korea, Dem. Rep.','continent']='Asia'
    df.loc[df.country == 'Micronesia, Fed. Sts.','continent']='Europe'
    df.loc[df.country == 'Macao, China','continent']='Asia'
    df.loc[df.country == 'Micronesia, Fed. Sts.','continent']='Oceania'
    df.loc[df.country == 'Netherlands Antilles','continent']='Europe'
    df.loc[df.country == 'Reunion','continent']='Europe'
    df.loc[df.country == 'Serbia and Montenegro','continent']='Europe'
    df.loc[df.country == 'West Bank and Gaza','continent']='Asia'

    # Remove NaN
    #df.dropna(axis=0, inplace=True)

    return df

def make_graph_bar(alcohol_mean, width):
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
        'title': "<b>대륙별 수치 비교</b> <br><sup>소득이 높을수록 알코올 소비가 가장 높다.</sup>",
        'height': 420,
        'width': width,
    }

    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div

def make_graph_scatter(df, width):
    graphs = []
    graphs.append(
        go.Scatter(x=df.incomeperperson.tolist(), y=df.urbanrate.tolist(),
            name='Primary Product',
            mode='markers',
            marker_color='indianred',
                   
            hovertemplate =
            '<i>GDP</i>: $%{x:.2f}'+
            '<br><b>Urbanrate</b>: %{y}<br>'+
            '<b>%{text}</b>',
                    text=df['country'])
    )
    layout = {
        'height': 420,
        'width': width,
        'title': '<b>GDP가 높은 나라일수록 도시 인구 비율이 높다.</b>',
        'xaxis_title': "Income per person",
        'yaxis_title': "Urban Rate"
    }

    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div


def make_graph_pie(df):
    graphs = []
    graphs.append(
        go.Pie(labels=df.continent.unique(),
                 values=df.groupby(by='continent').country.count().tolist()
                )
    )
    layout = {
        'height': 420,
        'width': 550,
        'title': '<b>대륙별 나라 수</b><br><sup>아시아 대륙이 나라 수가 가장 많다.</sup>',
        'xaxis_title': "Income per person",
        'yaxis_title': "Urban Rate"
    }

    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div

def make_graph_top5(df):
    alcohol_max = df.nlargest(5, 'alcconsumption')
    alcohol_min = df.nsmallest(5, 'alcconsumption')


    country_list = alcohol_max.country.tolist()
    min_list = alcohol_min.country.tolist()
    alcohol_list = alcohol_max.alcconsumption.tolist()
    alcohol_min_list = alcohol_min.alcconsumption.tolist()

    country_list.extend(min_list)
    alcohol_list.extend(alcohol_min_list)

    colors = ['lightsalmon',] * 5 + ['crimson',] * 5

    graphs = []
    graphs.append(
        go.Bar(
                y=country_list, 
                x=alcohol_list,
                orientation='h', 
                texttemplate="%{x}",textposition='outside',
                marker_color=colors )
    )
    layout = {
        'height': 420,
        'width': 550,
        'title': '<b>알코올 소비가 가장 낮은/높은 국가 TOP5</b><br><sup>전 세계에서 한국이 2위를 차지했다.</sup>',
        'xaxis_title': "Alcohol Consumption",
        'barmode': 'stack'
    }
    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div



# Create your views here.-----------------------------------------------------
def index(request):

    new_df = getNewDF(df_alcohol, df_continents)

    # Group by Continent
    df_mean_continent = new_df.groupby(by='continent').mean()

    # Send to HTML Template
    contents={}
    contents['csv_df'] = df_alcohol
    contents['plot_bar'] = make_graph_bar(df_mean_continent, 1000)
    contents['plot_pie'] = make_graph_pie(new_df)
    contents['plot_bar_top'] = make_graph_top5(df_alcohol)

    return render(request, 'index.html', contents)

def step1(request):
    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    new_df = getNewDF(df_alcohol, df_continents)

    # Group by Continent
    df_mean_continent = new_df.groupby(by='continent').mean()

    contents={}
    
    contents['df_isna'] = df_alcohol.isna().sum().tolist()
    contents['csv_df'] = df_alcohol.head(5)
    contents['df_continents'] = df_continents.head(5)
    contents['df_mean_continent'] = df_mean_continent
    return render(request, 'step1.html', contents)

def step2(request):
    df_alcohol = pd.read_csv(path_alcohol)

    contents={}
    contents['plot_corr'] = make_graph_corr(df_alcohol)
    return render(request, 'step2.html', contents)


def step3(request):
    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    new_df = getNewDF(df_alcohol, df_continents)

    # Group by Continent
    df_mean_continent = new_df.groupby(by='continent').mean()

    # Send to HTML Template
    contents={}
    contents['plot_bar'] = make_graph_bar(df_mean_continent, 1000)
    contents['plot_scatter'] = make_graph_scatter(df_alcohol, 1000)
    return render(request, 'step3.html', contents)

def tables(request):
    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    new_df = getNewDF(df_alcohol, df_continents)

    contents={}
    contents['csv_df'] = new_df
    return render(request, 'tables.html', contents)


def charts(request):
    df_alcohol = pd.read_csv(path_alcohol)
    df_continents = pd.read_csv(path_continents)

    new_df = getNewDF(df_alcohol, df_continents)

    # Group by Continent
    df_mean_continent = new_df.groupby(by='continent').mean()

    contents={}
    contents['plot_corr'] = make_graph_corr(df_alcohol)
    contents['plot_bar'] = make_graph_bar(df_mean_continent, 1200)
    contents['plot_scatter'] = make_graph_scatter(df_alcohol, 550)
    contents['plot_pie'] = make_graph_pie(new_df)
    contents['plot_bar_top'] = make_graph_top5(df_alcohol)
    
    return render(request, 'charts.html', contents)