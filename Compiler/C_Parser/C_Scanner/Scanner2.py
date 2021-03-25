#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 12:40:42 2021

@author: tim
"""

class Scanner():
    
    def __init__(self,Path,File,TokenFile):
        self.Path = Path
        self.Tokens = self.ReadTokensFile(TokenFile)
        self.fileString = self.ReadSourceFile(File)
        self.fileLength = len(self.fileString)
        print(self.fileString)
        print(self.Tokens)
        
        
    def generateTokenizedSource():    
        x = 6
        return 0
        
        


    def ReadSourceFile(self,File):
         with open(self.Path + File,"r") as fileHandler:
            fileString = fileHandler.read()
         far
         return fileString



Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
File = "HelloWorld.c"
Tokens = "Tokens.t"
Scanner = Scanner(Path,File,Tokens)