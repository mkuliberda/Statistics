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
import csv
from pathlib import Path

timeh=[]
pressure=[]
humidity=[]
temperature=[]
dew_point=[]


today=datetime.datetime.now()
latestLog = '/home/pi/Desktop/Environment/Environment_' + str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '.csv'
global logsCount
global logs
#print(latestLog)

class envStatistics(object):

    
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
                
    def run(self):

        while self._running:
            print("running...")
            
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
                    plots = list(csv.reader(csvfile, delimiter=','))
                    for row in plots:
                        timeh[i].append(int(row[1]))
                        pressure[i].append(float(row[2]))
                        humidity[i].append(float(row[3]))
                        temperature[i].append(float(row[4]))
                        dew_point[i].append(float(row[5]))
        else:
            print('no logs available')
            
    def getLogsList(self):
        tempList = glob.glob("/home/pi/Desktop/Environment/*.csv")
        #print(tempList)
        if latestLog in tempList:
            tempList.remove(latestLog)
        return tempList

    def createPlots(self):
        #print(nbr)
        for i in range(logsCount):
            plot.figure(i, figsize=(16, 8))
            plot.suptitle(logs[i])

            plot.subplot(221)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('pressure [hPa]')
            plot.plot(timeh[i],pressure[i])

            plot.subplot(222)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('temperature [C]')
            plot.plot(timeh[i],temperature[i])

            plot.subplot(223)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('humidity [%]')
            plot.plot(timeh[i],humidity[i])

            plot.subplot(224)
            plot.xlabel('time [hhmmss]')
            plot.ylabel('dew point [C]')
            plot.plot(timeh[i],dew_point[i])

            plot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
            plot.style.use('classic')
        plot.show(block=False)

test = envStatistics()
test.readLogs()
test.createPlots()

input("Press Enter to exit ...")
exit()


            
        
                
  
