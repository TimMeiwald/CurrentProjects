#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:25:18 2021

@author: tim
"""

# Purpose: Scanner, part of Lexer. Defacto read in C file, tokenize results

class Scanner():
    
    def __init__(self,Path,File):
        with open(Path + File,"r") as fileHandler:
            self.fileString = fileHandler.read()
        
        self.fileLength = len(self.fileString)
        self.StripComments()
        self.StripSpaces()


    def StripComments(self):
        for i in range(0,self.fileLength):
            if(self.fileString[i:i+2] == "//"):
                Start = i
                End = self.findEOL(Start)
                self.fileString = self.fileString[0:Start] + self.fileString[End:]
                
            if(self.fileString[i:i+2] == "/*"):
                Start = i
                End = self.findStringPosition("*/",Start)
                self.fileString = self.fileString[0:Start] + self.fileString[End:]

        return self.fileString
    
    def findEOL(self,Start):
        for i in range(Start,self.fileLength):
            if(self.fileString[i:i+1] == "\n"):
                End = i+1
                return End
            
    def findStringPosition(self, String, Start = 0):
        stringLength = len(String)
        for i in range(Start,self.fileLength):
           if(self.fileString[i:i+stringLength] == String):
               End = i+stringLength
               return End
          
    def StripSpaces(self):
        String = self.fileString.replace(" ","")
        String = String.replace("\n","")
        self.fileString = String
        return String
                

Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
File = "HelloWorld.c"
Scanner = Scanner(Path,File)
#x = Scanner.StripComments()
#y = Scanner.StripSpaces()