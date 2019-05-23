#!/usr/bin/python
# import necessary packages
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plot
import argparse
import sys
import glob
from datetime import datetime, timedelta
import time
import matplotlib
import csv
from pathlib import Path
# prettier plotting with seaborn
import seaborn as sns;
import matplotlib.dates as mdates
import matplotlib.ticker as tick
from matplotlib.widgets import CheckButtons


plots_range = 'standard'
log_path = ''

parser = argparse.ArgumentParser()
parser.add_argument('--today', help='plot only todays log',
                    action='store_true')
parser.add_argument('--yesterday', help='plot only yesterdays log',
                    action='store_true')
parser.add_argument('--path', dest='file', required=False, help='plot only specific log',
                    type=lambda f: open(f))
parser.add_argument('--all', help='plot all avbl logs',
                    action='store_true')
parser.add_argument('--standard', help='plot all avbl logs with the exception of todays one',
                    action='store_true')


args = parser.parse_args()
if args.today:
    plots_range = 'today'
    
elif args.yesterday:
    plots_range = 'yesterday'
    
elif args.all:
    plots_range = 'all'

elif args.standard:
    plots_range = 'standard'

elif args.file.name is not None:
    log_path = args.file.name
    plots_range = 'path'
    




# make figures plot inline
plot.ion()

sns.set(font_scale=1.1)
sns.set_style("whitegrid")

def getLogsList(path, plots = 'today'):

    if plots == 'standard':
        today=datetime.now()
        temp_list = glob.glob("/home/pi/Desktop/Environment/*.csv")
        today_log = '/home/pi/Desktop/Environment/Environment_' + str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '.csv'
        if today_log in temp_list:
            temp_list.remove(today_log)
            return temp_list
        
    elif plots == 'today':
        today=datetime.now()
        today_log = '/home/pi/Desktop/Environment/Environment_' + str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '.csv'
        return [today_log]

    elif plots == 'yesterday':
        yest_temp = datetime.now() - timedelta(days=1)
        yesterday_log = '/home/pi/Desktop/Environment/Environment_' + str(yest_temp.day) + '_' + str(yest_temp.month) + '_' + str(yest_temp.year) + '.csv'
        return [yesterday_log]

    elif plots == 'all':
        temp_list = glob.glob("/home/pi/Desktop/Environment/*.csv")
        return temp_list

    elif plots == 'path':
        return [path]

def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plot.draw()


files = getLogsList(log_path, plots_range)

#def createPlots(files):

logs = []
# import file into pandas dataframe
for i in range(len(files)):
    boulder = pd.read_csv(files[i],parse_dates = ['Time'],index_col = ['Time'])
    logs.append(boulder)
    # just for checking and testing, to be removed in future
    #print(logs[i].dtypes)


timeFmt = mdates.DateFormatter('%H:%M')
pressFmt = tick.FormatStrFormatter('%.2f')
temp_humFmt = tick.FormatStrFormatter('%.1f')
pmFmt = tick.FormatStrFormatter('%d')
C=20 #TODO color on scatter plots not working now

#check = []
for i in range(len(logs)):
    # create the plot space upon which to plot the data
    fig = plot.figure(i, figsize=(20,20))
    plot.suptitle(files[i])


    ax1 = fig.add_subplot(2,2,1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2,2,3)
    ax4 = fig.add_subplot(2,2,4)


    # add the x-axis and the y-axis to the plot
    ax1.plot(logs[i].index.values,
            logs[i]['Pressure'],
            color = 'blue')
    ax1.scatter(logs[i].index.values,
                logs[i]['Pressure'], C)

    ax1.xaxis.set_major_formatter(timeFmt)
    ax1.yaxis.set_major_formatter(pressFmt)

    # rotate tick labels
    plot.setp(ax1.get_xticklabels(), rotation=45)

    # set title and labels for axes
    ax1.set(xlabel="Time",
           ylabel="Pressure [hPa]");


    

    ax2.plot(logs[i].index.values,
            logs[i]['Humidity'],
             color = 'green')
    ax2.scatter(logs[i].index.values,
                logs[i]['Humidity'], C)

    ax2.xaxis.set_major_formatter(timeFmt)
    ax2.yaxis.set_major_formatter(temp_humFmt)


    # rotate tick labels
    plot.setp(ax2.get_xticklabels(), rotation=45)

    # set title and labels for axes
    ax2.set(xlabel="Time",
           ylabel="Humidity [%]");


    


    ax3.plot(logs[i].index.values,
            logs[i]['Temperature'],
            color = 'red', label = 'Temperature')
    ax3.plot(logs[i].index.values,
            logs[i]['Dew_point'],
            color = 'purple', label = 'Dew point')

    ax3.scatter(logs[i].index.values,
                logs[i]['Temperature'], C, label = '_Temperature')
    ax3.scatter(logs[i].index.values,
                logs[i]['Dew_point'], C, label = '_Dew point')


    ax3.xaxis.set_major_formatter(timeFmt)
    ax3.yaxis.set_major_formatter(temp_humFmt)
    legend = ax3.legend( shadow=True)


    # rotate tick labels
    plot.setp(ax3.get_xticklabels(), rotation=45)

    # set title and labels for axes
    ax3.set(xlabel="Time",
           ylabel="Temperature, Dew point [C]");


    

    l0, = ax4.plot(logs[i].index.values,
            logs[i]['PM1'],
            color = 'yellow', label = 'PM1')
    l1, = ax4.plot(logs[i].index.values,
            logs[i]['PM2.5'],
            color = 'orange', label = 'PM2.5')
    l2, = ax4.plot(logs[i].index.values,
            logs[i]['PM10'],
            color = 'chocolate', label = 'PM10')
    
    #s0, = ax4.scatter(logs[i].index.values,
    #            logs[i]['PM1'], C, label = '_PM1')
    #s1, = ax4.scatter(logs[i].index.values,
    #            logs[i]['PM2.5'], C, label = '_PM2.5')
    #s2, = ax4.scatter(logs[i].index.values,
    #            logs[i]['PM10'], C, label = '_PM10')

    lines = [l0, l1, l2]

    # Make checkbuttons with all plotted lines with correct visibility
    rax = plot.axes([0.5, 0.35, 0.05, 0.10])
    labels = [str(line.get_label()) for line in lines]
    visibility = [line.get_visible() for line in lines]
    check = CheckButtons(rax, labels, visibility)
    check.on_clicked(func)


    ax4.xaxis.set_major_formatter(timeFmt)
    ax4.yaxis.set_major_formatter(pmFmt)
    legend = ax4.legend(shadow=True)


    # rotate tick labels
    plot.setp(ax4.get_xticklabels(), rotation=45)

    # set title and labels for axes
    ax4.set(xlabel="Time",
           ylabel="PM1, PM2.5, PM10 [ug/m3]");

    
    plot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
    plot.show(block=False)



#createPlots(paths)



input("Press Enter to exit ...")
exit()

