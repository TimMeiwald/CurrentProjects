#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:23:30 2021

@author: tim
"""

import matplotlib.pyplot as plt



import FileManipulation


path = "/home/tim/Documents/Python Scripts/FTSE100StockData"
file = "GSK.L"


x = FileManipulation.Files.readYahooFinanceCSV(path, file)

#plt.plot(range(len(x["Date"])),x["Open"])
#plt.plot(range(len(x["Date"])),x["Close"])
#plt.plot(range(len(x["Date"])),x["High"])
#plt.plot(range(len(x["Date"])),x["Low"])

MaxDiff = []
for i in range(len(x["Date"])):
    MaxDiff.append(x["High"][i]- x["Low"][i])
    
OpenCloseDiff = []
    
for i in range(len(x["Date"])):
    OpenCloseDiff.append(x["Close"][i]- x["Open"][i])

DailyAverage = []
for i in range(len(x["Date"])):
    DailyAverage.append((x["Close"][i] + x["Open"][i])/2.)

WeeklyAverage = []
for i in range(3,len(x["Date"])-5):
    WeeklyAverage.append(sum(x["Open"][i:i+5])/5)

Variance = []
for i in range(0,len(x["Date"])-8):
    Variance.append(((x["High"][i] - WeeklyAverage[i]) + (WeeklyAverage[i] - x["Low"][i]))/2.)


#plt.plot(range(len(x["Date"])-8),WeeklyAverage)
plt.plot(range(len(x["Date"])-8),Variance)
#plt.plot(range(len(x["Date"])),DailyAverage)
#plt.plot(range(len(x["Date"])),x["High"])
#plt.plot(range(len(x["Date"])),x["Low"])
#plt.plot(range(len(x["Date"])),x["Volume"])