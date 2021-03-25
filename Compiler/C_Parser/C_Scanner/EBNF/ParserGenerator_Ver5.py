#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:09:18 2021

@author: tim
"""
from EBNFParser_ver2 import EBNFParser

class EBNFParserGenerator():
    
    def __init__(self,Path,GrammarFile):
        self.VarNames = []
        self.IndentLevel = 0
        self.Scope = 1
        self.Commas = 0
        self.Count = -1
        self.x = self.GetScannedGrammar(Path,GrammarFile)
        self.Tokenstream = self.x[0]
        self.Dict_KeyToValue = self.x[1]
        self.Dict_ValueToKey = self.x[2]
        self.Results = []
        self.GenerateParser()
        
    def GetScannedGrammar(self, Path, GrammarFile):
        TokenList = "EBNFTokenList.txt"
        GrammarParser = EBNFParser(Path,GrammarFile,TokenList)
        GrammarStream = GrammarParser.ParsedGrammar
        Dict_KeyToValue =  GrammarParser.Dict_KeyToValue
        Dict_ValueToKey = GrammarParser.Dict_ValueToKey
        return GrammarStream, Dict_KeyToValue, Dict_ValueToKey
    
    
    
    def GenerateParser(self):
        
        Start, End = 0, 0
        Rules = []
        for i in self.Tokenstream:
            if(i == "START RULE"):
                Start = End 
            if(i == "END RULE"):
                Rules.append(self.Tokenstream[Start+1:End])
            End += 1    
        
        for i in Rules:
            self.Scope = 1
            self.IndentLevel = 0
            self.Commas = 0
            self.ParseRule(i)

    def ParseRule(self,Rule):
        Rule = self.StartRule(Rule)
        for i in Rule:
            self.Const(i)
            self.Var(i)
            self.Ops(i)
            
        self.EndRule(Rule)
    
    def Const(self,Token):
        if(Token[0] == "CONST"):
            self.WriteToResultStringIndented("if(Token[{}] == {}):".format(self.Commas,Token[1]))
            
        
    def Var(self,Token):
        if(Token[0] == "VAR"):
            self.WriteToResultStringIndented("if(Rule_{}(Token[{}]) == True):".format(Token[1],self.Commas))

        
    def Ops(self,Token):
        if(Token[0] == "OP"):
            if(Token[1] == 9): #9 is ,
                self.Commas += 1
                self.IndentLevel += 1
            if(Token[1] == 12): #12 is |
                self.Commas = 0
                self.IndentLevel += 1
                self.WriteToResultStringIndented("return True")
                self.IndentLevel = self.Scope
        #########################################################
        # HANDLE REPETITION, SOMEHOW RECURSION OR SPLIT INTO BNF#
        #########################################################
    def StartRule(self,Rule):
        if(Rule[0][0] == "VAR" and Rule[1] == ("OP",11)):
            self.WriteToResultStringIndented("\ndef Rule_{}(Tokens):".format(Rule[0][1]))
            self.IndentLevel += 1
            return Rule[2:]
        else: 
            raise
    
    def EndRule(self,Rule):
        self.IndentLevel += 1
        self.WriteToResultStringIndented("return True")
        self.IndentLevel = 1
        self.WriteToResultStringIndented("return False")
    
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
x = EBNFParserGenerator(Path,GrammarFile)