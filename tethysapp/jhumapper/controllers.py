import os
import random
import string

import grids
import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import SelectInput

from .app import Jhumapper as App


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    select_layers = SelectInput(
        display_text='Select data layer',
        name='select-layers',
        multiple=False,
        original=True,
        initial='probability',
        options=(
            ('2018 Monthly Probabilities', 'probability'),
            ('Long Term Symptomatic Rate', 'sympt'),
            ('Long Term Asymptomatic Rate', 'asympt')
        )
    )
    select_plot_style = SelectInput(
        display_text='Plot results of boxes/polygons as:',
        name='select-plot-style',
        multiple=False,
        original=True,
        initial='median',
        options=(
            ('Median value', 'median'),
            ('Mean value', 'mean'),
            ('Summary Stats', 'sumstat'),
            ('Histograms', 'histogram')
        )
    )

    context = {
        "layers": select_layers,
        "plot_style": select_plot_style,
        "thredds_wms_base": App.get_custom_setting("thredds_wms_base"),
    }
    return render(request, 'jhumapper/home.html', context)


@login_required()
def query_values(request):
    """
    Controller for the app home page.
    """
    workspace_path = App.get_app_workspace().path
    data = dict(request.GET)
    print(data)
    stats = ('max', '75%', 'median', 'mean', '25%', 'min', 'values')

    ts = grids.TimeSeries(
        files=[os.path.join(workspace_path, 'Shigella_2018.nc4'), ],
        var='probability',
        dim_order=('time', 'lat', 'lon'),
        interp_units=False,
        stats=stats
    )

    if 'point[]' in data.keys():
        coords = data['point[]']
        ts = ts.point(None, float(coords[0]), float(coords[1]))
    elif 'rectangle[]' in data.keys():
        coords = data['rectangle[]']
        ts = ts.bound(
            (None, float(coords[0]), float(coords[1])),
            (None, float(coords[2]), float(coords[3])),
        )
    elif 'polygon' in data.keys():
        letters = string.ascii_lowercase
        tmpfile = ''.join(random.choice(letters) for i in range(10)) + '.json'
        tmppath = os.path.join(workspace_path, tmpfile)
        with open(tmppath, 'w') as f:
            f.write(str(data['polygon'][0]))
        ts = ts.shape(tmppath, behavior='dissolve')
    elif 'AdminDist' in data.keys():
        shppath = os.path.join(workspace_path, 'gadm36_levels_shp', 'gadm36_1.shp')
        ts = ts.shape(shppath, behavior='features', labelby='GID_1')
        ts = ts[[data['AdminDist'], ]]
    else:
        raise ValueError('Unrecognized query request')

    timesteps = pd.Index(pd.to_datetime(ts.datetime, unit="s")).strftime("%Y-%m").to_list()
    del ts['datetime']
    print(ts)

    return JsonResponse({
        'x': timesteps,
        'y': ts.values.flatten().tolist(),
        # 'max': ts['probability_max'].values.flatten().tolist(),
        # 'p75': ts['probability_75%'].values.flatten().tolist(),
        # 'median': ts['probability_median'].values.flatten().tolist(),
        # 'mean': ts['probability_mean'].values.flatten().tolist(),
        # 'p25': ts['probability_25%'].values.flatten().tolist(),
        # 'min': ts['probability_min'].values.flatten().tolist(),
        # 'values': ts['probability_values'].values.flatten().tolist(),
    })
