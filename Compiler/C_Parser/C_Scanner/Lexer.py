#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:42:19 2021

@author: tim
"""
import StandardScanner_pipe as Scanner
ScannerClass = Scanner.Scanner


        
class Lexer(ScannerClass):
    
    def __init__(self,Path,File,List):
        #Runs Scanner __init__
        super(Lexer,self).__init__(Path,File,List)
        self.Comment_OPEN = self.Dict_KeyToValue[b"//"]
        self.Comment_CLOSE = self.Dict_KeyToValue[b"\n"]
        self.String_OPEN = [self.Dict_KeyToValue[b"'"], self.Dict_KeyToValue[b'"']] 
        self.String_CLOSE = [self.Dict_KeyToValue[b"'"], self.Dict_KeyToValue[b'"'] ] 
        
        self.Result = self.StripAll()
        self.CloseFile()

    
    
    
    
    """
    def StripAll(self):
        i = b" "
        ResultsList = []
        Count = 0
        while i != b"EOF":
            i = self.TokenizerPipe()
            if(i == self.Comment_OPEN):
                self.StripComments()
            ResultsList.append(i)
            Count += 1
        return ResultsList
    
    def StripComments(self):
        i = ""
        while i != self.Comment_CLOSE:
            i = self.TokenizerPipe()
            print(i)
        return 0

   """
            

    
    def StripStrings(self):
        
        return 
        
    
Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
List = "List.txt"
File = "HelloWorld.c"
x = Lexer(Path,File,List)
y = x.Result
