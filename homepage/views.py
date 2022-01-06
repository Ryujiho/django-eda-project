from django.shortcuts import render, HttpResponse
import pandas as pd
import os
from pathlib import Path

# Create your views here.
def index(request):

    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'homepage', 'static', 'alcohol.csv')

    contents={}
    contents['csv_df'] = pd.read_csv(path)
    return render(request, 'index.html', contents)