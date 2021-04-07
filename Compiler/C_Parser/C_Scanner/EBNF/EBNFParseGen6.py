#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:14:08 2021

@author: tim
"""

from EBNFScanner import Scanner
#from StandardScanner_pipeVer2 import Scanner

class EBNFParser():
    
    def __init__(self,Path,GrammarFile,TokenList):
        self.GrammarFile = []
        self.Dict_KeyToValue, self.Dict_ValueToKey = {},{}
        self.ReadGrammarFile(Path,GrammarFile,TokenList)
        Result = []
        for i in self.GrammarFile:
            Result.append(i)
            if(i == 6):
                Result = []
            print(Result)
            if(i == 2):
                Result = []
            if(i == 3):
                Result = []
                
        
    def ReadGrammarFile(self,Path,GrammarFile,TokenList):
        scanner = Scanner(Path,GrammarFile,TokenList)
        i = b""
        while i != b"EOF":
            i = scanner.GetToken()
            self.GrammarFile.append(i)
        self.Dict_KeyToValue, self.Dict_ValueToKey = scanner.Dict_KeyToValue, scanner.Dict_ValueToKey 
        scanner.CloseFile()
        
    def WriteToResultStringIndented(self,String):
        debug = True
        if(debug == True):
            print("{}{}".format(self.Indent(),String))
        else:  
             String = "\n{}{}".format(self.Indent(),String)
             self.ResultString += String

    def Indent(self):
        return " "*self.IndentLevel*4




Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"
TokenList = "EBNFTokenList.txt"
x = EBNFParser(Path,GrammarFile,TokenList)