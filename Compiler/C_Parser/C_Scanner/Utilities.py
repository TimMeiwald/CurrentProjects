#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 14:42:18 2021

@author: tim
"""

def readFileToString(Path,File):
     with open(Path + File, "r") as fileHandler:
            fileString = fileHandler.read()
     return fileString

def findStringPosition(self, String, Start = 0):
    stringLength = len(String)
    for i in range(Start,self.fileLength):
       if(self.fileString[i:i+stringLength] == String):
           End = i+stringLength
           return End