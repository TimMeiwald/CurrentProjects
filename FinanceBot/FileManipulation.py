#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 10:42:29 2021

@author: tim
"""
import platform


class Files():
    
    
    
    def readFile(Path, File, HeaderExists = True, AsDict = False):
        if(type(HeaderExists) != bool):
            raise Exception("Header must take boolean value")

        if(platform.system() == "Linux"):
            with open(Path + "/" + File + ".csv","r") as openfile:
                
                if(HeaderExists == True and AsDict == False):
                    #Jumps file cursor forward one line since readline() does
                    #that anyway to skip the headers
                    openfile.readline()
                    
                filestring = openfile.read() 
                openfile.close()
                return filestring
        else: 
           raise Exception("This function has not yet been defined for this operating system")
        
        
        
        
    def readCSV(Path, File, HeaderExists = True,AsDict = False):
        #Assumes MxN sized CSV
        filestring = Files.readFile(Path,File, HeaderExists,AsDict)

        ValueList = []
        for line in filestring.split("\n"):
            linelist = line.split(",")
            ValueList.append(linelist)
        Cols = len(ValueList[0])
        Rows = len(ValueList)
        
        List = []
        Records = []
    
        for i in range(Cols):
            for j in range(Rows):
                List.append(ValueList[j][i])

        for k in range(Cols):
            Records.append(List[k*Rows:k*Rows + Rows])
            
        if(AsDict == True and HeaderExists == True):
            Dict = {}
            for k in range(Cols):
                ColumnName = Records[k][0]
                Records[k].remove(ColumnName)
                Dict[ColumnName] = Records[k]        
            Records = Dict
        return Records
    
    
    def readYahooFinanceCSV(Path, File):
        #Converts strings to floats where appropriate, i.e everywhere but date
      
        CSV = Files.readCSV(Path,File,HeaderExists = True, AsDict = True)
        for i in CSV:
            if(i != "Date"):
                for j in range(len(CSV[i])):
                    CSV[i][j] = float(CSV[i][j])
        return CSV


                
       
       

        
        
