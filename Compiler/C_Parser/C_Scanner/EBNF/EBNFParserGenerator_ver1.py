#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 15:39:03 2021

@author: tim
"""
from EBNFScanner import Scanner
from EBNFParser_ver2 import EBNFParser

class EBNFParserGenerator():
    
    def __init__(self,Path,GrammarFile):
        self.Position = 0
        self.EBNF_KeyToValue, self.EBNF_ValueToKey = {}, {}
        self.Cd = {}
        self.GrammarStream = []
        self.GetParsedGrammar(Path,GrammarFile)
        self.SeperateRules()
        self.Vars = self.GenerateRuleDict()
        self.Results = self.ParseRules()

        
    def GetParsedGrammar(self, Path, GrammarFile):
        TokenList = "EBNFTokenList.txt"
        GrammarParser = EBNFParser(Path,GrammarFile,TokenList)
        self.GrammarStream = GrammarParser.ParsedGrammar
        self.EBNF_KeyToValue =  GrammarParser.Dict_KeyToValue
        self.EBNF_ValueToKey = GrammarParser.Dict_ValueToKey
        
    def ConversionDict(self):
        self.Cd[12] = ","
        self.Cd[2] = "for i in range"
        self.Cd[3] = "\n    "
        
        
    def SeperateRules(self):
        Count = 0
        Pos = 0
        Rules = []
        for i in self.GrammarStream:
            if(i == "START RULE"):
                Pos = Count
            elif(i == "END RULE"):
                Rules.append(self.GrammarStream[Pos+1:Count])
            Count += 1
        self.GrammarStream = Rules
        
    def GenerateRuleDict(self):
        Vars = {}
        for i in self.GrammarStream:
            Vars[i[0][1]] = i[2:]
        return Vars
    
    def ParseRules(self):
        for i in self.Vars:
            Rule = ""
            print(i)
            self.ParseRule(self.Vars[i])
                
    def ParseRule(self,Rule):
        Len = len(Rule)
        print("\n")
        Result = ""
        self.Position = 0
        Result += self.TerminalRule(Rule,Len)
        print(Result)
        
        
    def TerminalRule(self,Rule,Len):
        ReturnVal = ""
        if(self.Position >= Len):
            print("]")
            return ""
        
        if(self.Position == 0):
            print("[")
        if(Rule[self.Position][0] == "CONST"):
            print(Rule[self.Position][1])
            self.Position += 1
            self.TerminalRule(Rule,Len)
            return ""
        elif(Rule[self.Position][1] == 12): #12 is |
            print(", ")
            self.Position += 1
            self.TerminalRule(Rule,Len)
            return ""
        elif(Rule[self.Position][0] == "VAR"):
            print(Rule[self.Position][1])
            self.Position += 1
            self.TerminalRule(Rule,Len)
            return ""
        elif(Rule[self.Position][1] == 9): # 9 is ,
            print("+")
            self.Position += 1
            self.TerminalRule(Rule,Len)
            return ""
        elif(Rule[self.Position][1] == 2): #2 is {
            self.Position += 1
            self.Repetition(Rule,Len)
            return ""
        elif(Rule[self.Position][1] == 3): #3 is }
            self.Position += 1
            self.TerminalRule(Rule, Len)
            
        #TODO FOR [,] and ()
        else:
            print(Rule[self.Position])
            print("Not all cases caught")
            return ""
        
    def Repetition(self,Rule,Len):
        if(self.Position >= Len):
            return ""
        print("] \n+ \n")
        print("CREATE SUBROUTINE FOR FOLLOWING REPETITIONS")
        print("START REPETITION")
        Repetition = []
        for i in range(self.Position,Len+1):
            if(Rule[i][1] == 3): #3 is }
                print(Repetition)
                print("END REPETITION \n+\n[")
                self.Position += 1
                self.TerminalRule(Rule, Len)
                return ""
            else:
                Repetition.append(Rule[self.Position][1])
                self.Position += 1


        
        
Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"

x = EBNFParserGenerator(Path,GrammarFile)