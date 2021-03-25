#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:13:24 2021

@author: tim
"""
import numpy as np
import FileUtilities as fileUtils
import csv
import FileManipulation 




class Stock():
    
    def __init__(self,Ticker, Exchange):
        self.path = "/home/tim/Documents/Python Scripts/FTSE100StockData"
        FullTicker = Ticker + Exchange
        record = open(self.path +"/" +FullTicker + ".csv", "r")
        self.data = FileManipulation.Files.readYahooFinanceCSV(self.path,FullTicker) 
        
    


class Market(Stock):
    
    def __init__(self):
        self.FTSE100List = np.genfromtxt('AuxiliaryCSVFiles/FTSE100Names.csv',delimiter = "'",dtype = str)
        for i in self.FTSE100List:
            i = Stock(i,".L")




        
        