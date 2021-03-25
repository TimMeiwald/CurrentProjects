#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:01:16 2021

@author: tim
"""
import os
import time as t
import numpy as np

def time():
    T = t.localtime()
    current_time = t.strftime("%H:%M:%S", T)
    return current_time

class fileUtilities():
    def __init__(self,path):
        self.path = path
    
    def checkFileInDir(self,TargetFile):
        dirEntries = os.listdir(self.path)
        if(TargetFile in dirEntries):
            return True
        else:
            return False
    def dirEntries(self):
        dirEntries = os.listdir(self.path)
        return dirEntries
    
    def deleteFileInDir(self,TargetFile,FileType):
        try:
            os.remove(self.path + "/"+TargetFile+FileType)
            print("Deleted {} at {}".format(TargetFile + FileType, time()))
        except:
            raise Exception("Deletion of File {} failed at {}".format(self.path + "/"+ TargetFile + FileType,time()))
    
    def deleteAllFilesInDir(self,TargetDir):
        try:
            dirEntries = os.listdir(self.path)
            for i in dirEntries:
                os.remove(self.path +"/"+i)
                print("Deleted {} at {}".format(i, time()))
            print("{} is now empty".format(self.path))
        except:
            raise Exception("Dir {} content deletion failed at {}".format(self.path,time()))
            
            
            
    def readCSVFile(self,TargetFile):
        CSVFile = np.genfromtxt(self.path+"/"+TargetFile+".csv",delimiter =",")
        return CSVFile
        

