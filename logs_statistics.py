#!/usr/bin/python

# Import packages
import os
import numpy as np
import argparse
import sys
import glob
import datetime
import time
import matplotlib.pyplot as plot
import matplotlib
import csv
from pathlib import Path

#logs format: (int)DDMMYY,(int)HHMMSS,(.2float)PRESSURE,(.2float)HUMIDITY,(0.2float)TEMPERATURE,(.2float)DEW_POINT

timeh=[]
pressure=[]
humidity=[]
temperature=[]
dew_point=[]


today=datetime.datetime.now()
latestLog = '/home/pi/Desktop/Environment/Environment_' + str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '.csv'
global logsCount
global logs
global plots
plots = 'standard'

parser = argparse.ArgumentParser()
parser.add_argument('--today_only', help='plot only todays log',
                    action='store_true')
parser.add_argument('--all', help='plot all avbl logs',
                    action='store_true')
  
args = parser.parse_args()
if args.today_only:
    plots = 'today'
elif args.all:
    plots = 'all'


class envStatistics(object):
                            
    def readLogs(self):

        global logsCount
        global logs
        
        logs = self.getLogsList()
        logsCount = len(logs)

        if logsCount > 0:
            for i in range(logsCount):
                timeh.append([])
                pressure.append([])
                humidity.append([])
                temperature.append([])
                dew_point.append([])
                with open(logs[i],'r') as csvfile:
                #data_initial = open(logs[i], "rU")
                #plots = list(csv.reader((line.replace('\0','') for line in data_initial)))
                    plots = list(csv.reader(csvfile, delimiter=','))
                    for row in plots:
                        timeh[i].append(row[0])
                        pressure[i].append(float(row[1]))
                        humidity[i].append(float(row[2]))
                        temperature[i].append(float(row[3]))
                        dew_point[i].append(float(row[4]))
        else:
            print('no logs available')
            
    def getLogsList(self):

        global plots
        tempList = glob.glob("/home/pi/Desktop/Environment/*.csv")

        if plots == 'standard':
            if latestLog in tempList:
                tempList.remove(latestLog)
                return tempList
            
        elif plots == 'today':
            return [latestLog]
        
        elif plots == 'all':
            return tempList         

    def createPlots(self):
        for i in range(logsCount):
            plot.figure(i, figsize=(16, 8))
            plot.suptitle(logs[i])

            plot.subplot(221)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('pressure [hPa]')
            plot.scatter(timeh[i],pressure[i])
            plot.plot(timeh[i],pressure[i],'C1')
            plot.gcf().autofmt_xdate()

            plot.subplot(222)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('temperature [C]')
            plot.scatter(timeh[i],temperature[i])
            plot.plot(timeh[i],temperature[i],'C3')

            plot.subplot(223)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('humidity [%]')
            plot.scatter(timeh[i],humidity[i])
            plot.plot(timeh[i],humidity[i],'C2')

            plot.subplot(224)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('dew point [C]')
            plot.scatter(timeh[i],dew_point[i])
            plot.plot(timeh[i],dew_point[i],'C4')

            plot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
            #plot.style.use('classic')
        plot.show(block=False)

stats = envStatistics()
stats.readLogs()
stats.createPlots()
print(today)
input("Press Enter to exit ...")
exit()


            
        
                
  
