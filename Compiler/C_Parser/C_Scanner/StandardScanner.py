#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 17:31:02 2021

@author: tim
"""


class Scanner():
    
    def __init__(self,Path,File,List, Whitespace = False):
        self.Dict_KeyToValue, self.Dict_ValueToKey = self.CreateDict(Path,List)
        self.Whitespace = Whitespace
        
        self.Result = self.Tokenizer(Path, File)
        #Whitespace = False ignores whitespace, if set True keeps whitespace, 
        #to allow for whitespace indented languages. 
        #False is default
    
    def Tokenizer(self,Path,File):
        ResultString = []
        String  = " "
        Cursor = 0
        with open(Path + File, "r") as fileHandler:
           for i in fileHandler.read():
               Cursor += 1
               if(String == " " or String == "\n"):
                   if(self.Whitespace == True):
                       ResultString.append(String)
                   String = ""
               elif("\n" in String):
                   ResultString.append(String[:-1])
                   if(self.Whitespace == True):
                       ResultString.append("\n") 
                   String = ""
               elif(String in self.Dict_KeyToValue):
                   ResultString.append(self.Dict_KeyToValue[String])
                   String = ""
               elif(String not in self.Dict_KeyToValue and i in self.Dict_KeyToValue):
                   ResultString.append(String)
                   String = ""
               String += i
        return ResultString
    
   

    
    def CreateDict(self,Path,List):
        with open(Path + List,"r") as fileHandler:
            tokens = fileHandler.read().split()
        tokens.sort(key = len)
        Dict_KeyToValue = {}
        Dict_ValueToKey = {}
        Count = 0
        for i in tokens:
            Dict_KeyToValue[i] = Count
            Dict_ValueToKey[Count] = i
            Count += 1
        return Dict_KeyToValue, Dict_ValueToKey
        
        
Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
List = "List.txt"
File = "HelloWorld.c"
x = Scanner(Path,File,List, Whitespace = True)
y = x.Result
y2 = x.Dict_ValueToKey
print("Nur Nummern, -1 heisst nicht ein token : \n", y)

#print(x.Dict_KeyToValue)
#print(x.Dict_ValueToKey)