from django.shortcuts import render
import pandas as pd

from io import BytesIO
import os, base64
from pathlib import Path

from plotly.offline import plot
import plotly.graph_objects as go

# Create Data Visualization
def make_graph_corr(alcohol_df):
    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    corr_df = alcohol_df.corr().apply(lambda x: round(x,2))

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Heatmap(df_to_plotly(corr_df),
                   hoverongaps = False)
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div

def make_graph(alcohol_df):
    graphs = []
    graphs.append(
        go.Scatter(
            x=alcohol_df.country.tolist(), 
            y=alcohol_df.alcconsumption.tolist(),
            mode='markers',
            marker_size=alcohol_df.pop.tolist()
            )
    )

    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return plot_div
    
# Create your views here.
def index(request):
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'homepage', 'static', 'alcohol.csv')
    df = pd.read_csv(path)

    # Send to HTML Template
    contents={}
    contents['csv_df'] = df
    contents['plot_div'] = make_graph_corr(df)
    #contents['plot_ddd'] = make_graph(df)

    return render(request, 'index.html', contents)


def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}