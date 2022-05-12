from re import template
from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.style import context
from .models import Green_by_date, Green_by_team, Emot_by_date, Num_check_ins
import pandas as pd
from datetime import datetime
from .utils import addData, getPlot, getStats

# first view for home page, including summary statistics
def ryg_dashboard(request):
    # gets summary statistics
    stats = getStats(True)
    # render main template along with stats
    return render(request, 'main.html', context={'status': {
        'status': 'home',
        'recent_green_perc': str(stats[0] * 100) + '%',
        'most_green_team': stats[1],
        'most_common_emotion': stats[2],
        'num_check_ins': stats[3],
    }})

# view for showing chart for green lights over time
def greens_by_date_view(request):
    # run function to add data to db here
    addData()
    # make query sets to get data
    green_by_date = Green_by_date.objects.all()
    green_by_date_x = [x.date for x in green_by_date]
    green_by_date_y = [x.percentage for x in green_by_date]
    # make plot and save as png image for later use
    getPlot(green_by_date_x, green_by_date_y, None, 0)

    return render(request, 'main.html', context={'status': 'greens_by_date'})

# view for showing green light percentages by team
def greens_by_team_view(request):
    # run function to add data to db here
    addData()
    # make query sets to get data
    green_by_team = Green_by_team.objects.all()
    green_by_team_x = [x.team for x in green_by_team]
    green_by_team_y = [x.percentage for x in green_by_team]
    getPlot(green_by_team_x, green_by_team_y, None, 1)

    return render(request, 'main.html', context={'status': 'greens_by_team'})

# view for showing most common emotions over time
def emot_by_date_view(request):
    # run function to add data to db here
    addData()
    # make query sets to get data
    emot_by_date = Emot_by_date.objects.all()
    emot_by_date_x = [x.date for x in emot_by_date]
    emot_by_date_y = [x.emotion for x in emot_by_date]
    emot_by_date_z = [x.percentage for x in emot_by_date]
    getPlot(emot_by_date_x[-5:], emot_by_date_y[-5:], emot_by_date_z[-5:], 2)

    return render(request, 'main.html', context={'status': 'emot_by_date'})

# view for showing number of check ins over time
def num_check_ins_view(request):
    # run function to add data to db here
    addData()
    # make query sets to get data
    num_check_ins = Num_check_ins.objects.all()
    num_check_ins_x = [x.date for x in num_check_ins]
    num_check_ins_y = [x.check_ins for x in num_check_ins]
    getPlot(num_check_ins_x, num_check_ins_y, None, 3)

    return render(request, 'main.html', context={'status': 'num_check_ins'})