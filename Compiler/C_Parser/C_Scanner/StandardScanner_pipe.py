#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:59:15 2021

@author: tim
"""

    

class Scanner():
    
    def __init__(self,Path,File,List):
        self.CurrentString = b" "
        self.WHITESPACE = -1
        self.NEWLINE = -2
        self.Datastream = []
        
        self.Dict_KeyToValue, self.Dict_ValueToKey = self.CreateDict(Path,List)
        self.fileHandler = self.OpenFile(Path,File)

        
    def OpenFile(self,Path,File):
        try:
            fileHandler = open(Path + File, "rb")
            return fileHandler
        except:
            raise Exception("Failed to open file, check path and file")
    
    def CloseFile(self):
        try:
            self.fileHandler.close()
            return 0
        except:
            raise Exception("Could not successfully close file")

    

    def TokenizerBuffer(self):
        Input = b" "
        while Input != b"EOF":
            Input = self.TokenizerPipe()
            self.Datastream.append(Input)
            ConcatenatedString = b""
            PreviousConcatenatedString = b""
            for i in self.Datastream:
                if(type(i) == int):
                    ConcatenatedString += self.Dict_ValueToKey[i]
                else:
                    ConcatenatedString += i
                if(ConcatenatedString not in self.Dict_KeyToValue):
                    if(type(self.Datastream[0]) != int):
                        PreviousConcatenatedString  = self.Datastream[0]
                    else:
                        PreviousConcatenatedString = self.Dict_KeyToValue[PreviousConcatenatedString] 
                    self.Datastream = [self.Datastream[-1]]
                    return PreviousConcatenatedString
                PreviousConcatenatedString = ConcatenatedString 
    


    def TokenizerPipe(self):
        String  = self.CurrentString
        i = b" "
        if(self.CurrentString != b""):
               i = self.fileHandler.read(1)
               if(String == b' '):
                   self.CurrentString = b"" + i
                   return self.WHITESPACE
                   
               elif(String == b"\n"):
                   self.CurrentString = b"" + i
                   return self.NEWLINE
               elif(b"\n" in String):
                   self.CurrentString = b"" + i
                   return String[:-1]

               elif(String in self.Dict_KeyToValue):
                   self.CurrentString = b"" + i
                   return self.Dict_KeyToValue[String]
               
               elif(String not in self.Dict_KeyToValue and i in self.Dict_KeyToValue):
                  self.CurrentString = b"" + i
                  return String

               self.CurrentString += i
               #Call itself until something valid can be given to Lexer
               return self.TokenizerPipe()
        else: 
            return b"EOF"

    
    def CreateDict(self,Path,List):
        with open(Path + List,"rb") as fileHandler:
            tokens = fileHandler.read().split()
        tokens.sort(key = len)
        Dict_KeyToValue = {}
        Dict_ValueToKey = {}

        Dict_KeyToValue[b"\n"] = self.NEWLINE
        Dict_KeyToValue[b" "] = self.WHITESPACE
        Dict_ValueToKey[self.WHITESPACE] = b" "
        Dict_ValueToKey[self.NEWLINE] = b"\n"
        Count = 0
        for i in tokens:
            Dict_KeyToValue[i] = Count
            Dict_ValueToKey[Count] = i
            Count += 1
        #print(Dict_KeyToValue, Dict_ValueToKey)
        return Dict_KeyToValue, Dict_ValueToKey
    


Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
List = "List.txt"
File = "HelloWorld.c"
x = Scanner(Path,File,List)
y = x.OpenFile(Path,File)
y2 = b""
ResultString = b""
while y2 != b"EOF":    
    y2 = x.TokenizerBuffer()
    if(type(y2) == int):
        ResultString += x.Dict_ValueToKey[y2]
    else:
        ResultString += y2
    print(y2)
ResultString = ResultString.decode("ASCII")
b = x.CloseFile()

