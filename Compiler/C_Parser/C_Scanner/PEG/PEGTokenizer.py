#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 19:31:28 2021

@author: tim
"""
import PEG3 as PEG

class PEGTokenizer():
    
    def __init__(self,filePath):
        pass

    def GetTokenizedGrammarFile(self):
        return self.ReadTextFile(filePath).split()
            
    def ReadTextFile(self,filePath):
        """Read Text file."""
        with open(filePath) as fileHandle:
            Text = fileHandle.read()
        return Text



class PEGParser():
    
    def __init__(self,filePath):
        self.grammarFile = PEGTokenizer(filePath).GetTokenizedGrammarFile()
        print(self.grammarFile)
    
filePath = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/PEG/PEGTestFile.txt"
PEGParser(filePath)