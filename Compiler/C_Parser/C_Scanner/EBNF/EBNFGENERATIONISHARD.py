#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:37:47 2021

@author: tim
"""
from EBNFScanner import Scanner



##########################################
#Assumption File is grammatically correct#
##########################################
class EBNFGrammar():
    
    
    def __init__(self,Path,GrammarFile,TokenList):
        self.scanner = Scanner(Path,GrammarFile,TokenList)
        self.TokenList = []
        self.Grammar(self.scanner)
        self.scanner.CloseFile()
            
    def Grammar(self,TokenList):
        for i in range(0,250):
            b = self.scanner.GetToken()
            print(b)

Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"
TokenList = "EBNFTokenList.txt"
x = EBNFGrammar(Path,GrammarFile,TokenList)

A, B = 0, 0
if(A == 0 
   or B == 0):
    print("whatever")