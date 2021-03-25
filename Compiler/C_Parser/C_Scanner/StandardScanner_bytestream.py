#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:05:37 2021

@author: tim
"""

class Scanner():
    
    def __init__(self,Path,File,List):
        self.Dict_KeyToValue, self.Dict_ValueToKey = self.CreateDict(Path,List)
        self.Result = self.Tokenizer(Path, File)

    
    def Tokenizer(self,Path,File):
        ResultString = []
        String  = b""
        WHITESPACE = -1
        NEWLINE = -2
        with open(Path + File, "rb") as fileHandler:
            i = b" "
            while(i != b""):
                i = fileHandler.read(1)
                if(String == b' '):
                    ResultString.append(WHITESPACE)
                    String = b""
                elif(String == b"\n"):
                    ResultString.append(NEWLINE)
                    String = b""
                elif(b"\n" in String):
                    ResultString.append(String[:-1])
                    ResultString.append(NEWLINE)
                    String = b""
                elif(String in self.Dict_KeyToValue):
                    ResultString.append(self.Dict_KeyToValue[String])
                    String = b""
                elif(String not in self.Dict_KeyToValue and i in self.Dict_KeyToValue):
                   ResultString.append(String)
                   String = b""
                String += i
        #Discards starting null char
        ResultString = ResultString[1:]
        return ResultString
    
   

    
    def CreateDict(self,Path,List):
        with open(Path + List,"rb") as fileHandler:
            tokens = fileHandler.read().split()
        tokens.sort(key = len)
        Dict_KeyToValue = {}
        Dict_ValueToKey = {}
        
        WHITESPACE = -1
        NEWLINE = -2
        Dict_KeyToValue[b"\n"] = NEWLINE
        Dict_KeyToValue[b" "] = WHITESPACE
        Dict_ValueToKey[-1] = b" "
        Dict_ValueToKey[-2] = b"\n"
        Count = 0
        for i in tokens:
            Dict_KeyToValue[i] = Count
            Dict_ValueToKey[Count] = i
            Count += 1
        return Dict_KeyToValue, Dict_ValueToKey
    
    
    
  
Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
List = "List.txt"
File = "HelloWorld.c"
x = Scanner(Path,File,List)
y = x.Result
y2 = x.Dict_ValueToKey
y3 = x.Dict_KeyToValue
