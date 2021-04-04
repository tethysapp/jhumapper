import grids

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
        ('Shigella_Probability_2018_Jan.nc', 'Jan'),
        ('Shigella_Probability_2018_Feb.nc', 'Feb'),
        ('Shigella_Probability_2018_Mar.nc', 'Mar'),
        ('Shigella_Probability_2018_Apr.nc', 'Apr'),
        ('Shigella_Probability_2018_May.nc', 'May'),
        ('Shigella_Probability_2018_Jun.nc', 'Jun'),
        ('Shigella_Probability_2018_Jul.nc', 'Jul'),
        ('Shigella_Probability_2018_Aug.nc', 'Aug'),
        ('Shigella_Probability_2018_Sep.nc', 'Sep'),
        ('Shigella_Probability_2018_Oct.nc', 'Oct'),
        ('Shigella_Probability_2018_Nov.nc', 'Nov'),
        ('Shigella_Probability_2018_Dec.nc', 'Dec'),
        ('Shigella_Probability_LTM_Asymptomatic.nc', 'Asymptomatic'),
        ('Shigella_Probability_LTM_Symptomatic.nc', 'Symptomatic')
    )
    select_layers = SelectInput(
        display_text='Select data layer',
        name='select-layers',
        multiple=False,
        original=True,
        initial='Jan',
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
    print(request.GET)
    print(dict(request.GET))
    data = request.GET

    if 'point' in data.keys():
        print('point')
    elif 'rectangle' in data.keys():
        print('rect')
    elif 'polygon' in data.keys():
        print('poly')

    return JsonResponse(data)
