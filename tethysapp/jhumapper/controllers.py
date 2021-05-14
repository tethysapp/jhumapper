import os
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
    schigellafiles = (
        ('2018 Monthly Probability', 'probability'),
        ('Long Term Symptomatic Rate', 'sympt'),
        ('Long Term Asymptomatic Rate', 'asympt')
    )
    select_layers = SelectInput(
        display_text='Select data layer',
        name='select-layers',
        multiple=False,
        original=True,
        initial='probability',
        options=schigellafiles
    )

    context = {
        "layers": select_layers,
        "thredds_wms_base": App.get_custom_setting("thredds_wms_base"),
    }
    return render(request, 'jhumapper/home.html', context)


@login_required()
def query_values(request):
    """
    Controller for the app home page.
    """
    data = dict(request.GET)

    timeseries_obj = grids.TimeSeries(
        files=[os.path.join(App.get_app_workspace().path, 'Shigella_2018.nc4'), ],
        var='probability',
        dim_order=('time', 'lat', 'lon'),
        interp_units=False,
    )

    if 'point[]' in data.keys():
        coords = data['point[]']
        ts = timeseries_obj.point(None, float(coords[0]), float(coords[1]))
    elif 'rectangle[]' in data.keys():
        coords = data['rectangle[]']
        ts = timeseries_obj.bound(
            (None, float(coords[0]), float(coords[1])),
            (None, float(coords[2]), float(coords[3])),
        )
    # elif 'polygon' in data.keys():
    #     ts = None
    else:
        raise ValueError('Unrecognized query request')

    # this is a work around for a bug in pandas handling dates as strings
    # https://github.com/pandas-dev/pandas/issues/32264
    ts.index = pd.Index(pd.to_datetime(ts.datetime, unit="s")).strftime("%Y-%m")
    del ts['datetime']

    return JsonResponse({
        'x': ts.index.to_list(),
        'y': ts.values.flatten().tolist(),
    })
