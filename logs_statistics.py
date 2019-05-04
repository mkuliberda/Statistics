#!/usr/bin/python
# import necessary packages
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plot
import argparse
import sys
import glob
import datetime
import time
import matplotlib
import csv
from pathlib import Path
# prettier plotting with seaborn
import seaborn as sns;
import matplotlib.dates as mdates
import matplotlib.ticker as tick


plots_range = 'standard'

parser = argparse.ArgumentParser()
parser.add_argument('--today_only', help='plot only todays log',
                    action='store_true')
parser.add_argument('--all', help='plot all avbl logs',
                    action='store_true')
  
args = parser.parse_args()
if args.today_only:
    plots_range = 'today'
elif args.all:
    plots_range = 'all'


# make figures plot inline
plot.ion()

# set standard plot parameters for uniform plotting
#plot.rcParams['figure.figsize'] = (6, 6)

sns.set(font_scale=1.1)
sns.set_style("whitegrid")

def getLogsList(plots = 'standard'):

    today=datetime.datetime.now()
    temp_list = glob.glob("/home/pi/Desktop/Environment/*.csv")
    today_log = '/home/pi/Desktop/Environment/Environment_' + str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '.csv'


    if plots == 'standard':
        if today_log in temp_list:
            temp_list.remove(today_log)
            return temp_list
        
    elif plots == 'today':
        return [today_log]
    
    elif plots == 'all':
        return temp_list         

def createPlots(files):

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


    for i in range(len(logs)):
        # create the plot space upon which to plot the data
        fig = plot.figure(i, figsize=(20,20))
        plot.suptitle(files[i])


        #fig, ax = plot.subplots(figsize = (20,20))
        ax1 = fig.add_subplot(2,2,1)
        ax2 = fig.add_subplot(2,2,2)
        ax3 = fig.add_subplot(2,2,3)
        ax4 = fig.add_subplot(2,2,4)


        # add the x-axis and the y-axis to the plot
        ax1.plot(logs[i].index.values,
                logs[i]['Pressure'],
                color = 'blue')
        ax1.scatter(logs[i].index.values,
                    logs[i]['Pressure'])

        ax1.xaxis.set_major_formatter(timeFmt)
        ax1.yaxis.set_major_formatter(pressFmt)

        # rotate tick labels
        plot.setp(ax1.get_xticklabels(), rotation=45)

        # set title and labels for axes
        ax1.set(xlabel="Time",
               ylabel="Pressure");

        ax2.plot(logs[i].index.values,
                logs[i]['Humidity'],
             color = 'green')
        ax2.scatter(logs[i].index.values,
                    logs[i]['Humidity'])

        ax2.xaxis.set_major_formatter(timeFmt)
        ax2.yaxis.set_major_formatter(temp_humFmt)


        # rotate tick labels
        plot.setp(ax2.get_xticklabels(), rotation=45)

        # set title and labels for axes
        ax2.set(xlabel="Time",
               ylabel="Humidity");


        ax3.plot(logs[i].index.values,
                logs[i]['Temperature'],
                color = 'red')
        ax3.scatter(logs[i].index.values,
                    logs[i]['Temperature'])

        ax3.xaxis.set_major_formatter(timeFmt)
        ax3.yaxis.set_major_formatter(temp_humFmt)

        # rotate tick labels
        plot.setp(ax3.get_xticklabels(), rotation=45)

        # set title and labels for axes
        ax3.set(xlabel="Time",
               ylabel="Temperature");

        ax4.plot(logs[i].index.values,
                logs[i]['Dew_point'],
                color = 'purple')
        ax4.scatter(logs[i].index.values,
                    logs[i]['Dew_point'])

        ax4.xaxis.set_major_formatter(timeFmt)
        ax4.yaxis.set_major_formatter(temp_humFmt)

        # rotate tick labels
        plot.setp(ax4.get_xticklabels(), rotation=45)

        # set title and labels for axes
        ax4.set(xlabel="Time",
               ylabel="Dew point");
        
        plot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
        plot.show(block=False)

paths = getLogsList(plots_range)
createPlots(paths)

input("Press Enter to exit ...")
exit()

