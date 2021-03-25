#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 12:23:24 2021

@author: tim
"""
from EBNFParser_ver2 import EBNFParser


class EBNFParserGenerator():
    
    def __init__(self,Path,GrammarFile):
        self.IndentLevel, self.Offset = 0, 1
        self.RulesList = []
        x = self.GetParsedGrammar(Path,GrammarFile)
        TokenStream = x[0]
        self.Dict_KeyToValue = x[1]
        self.Dict_ValueToKey = x[2]
        Rules = self.SplitRules(TokenStream)
        Rules = self.ParseRules(Rules)
        
        
    def GetParsedGrammar(self, Path, GrammarFile):
        TokenList = "EBNFTokenList.txt"
        GrammarParser = EBNFParser(Path,GrammarFile,TokenList)
        GrammarStream = GrammarParser.ParsedGrammar
        Dict_KeyToValue =  GrammarParser.Dict_KeyToValue
        Dict_ValueToKey = GrammarParser.Dict_ValueToKey
        return GrammarStream, Dict_KeyToValue, Dict_ValueToKey
        
    
                
    def SplitRules(self,TokenStream):
        Start, End = 0,0
        Rules = []
        for i in TokenStream:
            if(i == "START RULE"):
                Start = End + 1
            elif(i == "END RULE"):
                Rules.append(TokenStream[Start:End])
            End += 1
        return Rules
    
    
    def ParseRules(self,Rules):
        TrueCount = 0 #Rules successfully parsed
        FalseCount = 0 # Failed parsings to prevent infinite loop
        TotalCount = -1
        while TrueCount < len(Rules): 
            if(FalseCount >= 1000):
                raise Exception("Long running process, exiting")
            #Hardcoded 1000 means no more than 1000 correct rules and less false rules
            TotalCount +=1
            i = TotalCount
            if(TotalCount == len(Rules) -1):
                TotalCount = -1
            #Above keep trying rules until enough stick, basically exceptions 
            #happen if their is an undefined variable. 
            #So parsing has to complete in correvt order which in EBNF
            #Also enforces correct read order if EBNF correct
            try:
                self.ParseRule(Rules[i])
                self.RulesList.append(self.CurrentVar)
                print("Successfully created rule: {}".format(self.CurrentVar))
                TrueCount += 1
            except ValueError:
                FalseCount += 1
            except:
                raise
        print("All rules successfully created")
        
        return 0
                
                
    def ParseRule(self,Rule):
        
        Rule = self.Start(Rule)
        self.MainLoop(Rule)
        
    
    def Consts(self,TokenVal):
        self.PrintIndented("if(Token == {})".format(TokenVal))
        
    def Ops(self,TokenVal):
        if(TokenVal == 12): #12 is | or OR
            # Returns to function level indentation on or, unless offset has
            #been modified by e.g {} which indicates a repetition aka for loop
            self.IdentLevel += 1
            self.PrintIndented("return True")
            self.IdentLevel -= 1
            self.IdentLevel = self.Offset
        if(TokenVal == 9): #9 is , which is concat
            # if , then it means first token followed by second token etc
            #so by changing Identlevel we schain the if statements
            self.IdentLevel += 1
        if(TokenVal == 6): #6 is ;, aka end of statement
            self.IdentLevel += 1
            self.PrintIndented("return True")
            self.IdentLevel = 1
            self.PrintIndented("return False")
            
            
    def Vars(self,TokenVal):
        if(TokenVal not in self.RulesList and TokenVal != self.CurrentVar):
            print("Undefined Variable: '{}' in Rule_{}".format(TokenVal,self.CurrentVar))
            raise ValueError("Undefined Variable")
            
        self.PrintIndented("if(Rule_{}(Token) == True)".format(TokenVal))
    
    def Tokens(self,Token):
        TokenType, TokenVal = Token[0],Token[1]
        if(TokenType == "CONST"):
            self.Consts(TokenVal)
        elif(TokenType == "OP"):
            self.Ops(TokenVal)
        elif(TokenType == "VAR"):
            self.Vars(TokenVal)
        else:
            raise Exception("Should never get here")

    def MainLoop(self,Rule):
        for i in Rule:
            self.Tokens(i)
            
           



    def Start(self,Rule):
        self.Offset = 1
        self.IdentLevel = 0
        self.CurrentVar = ""
        if(Rule[0][0] == "VAR" and Rule[1][0] == "OP" and Rule[1][1] == 11):
            self.PrintIndented("\ndef Rule_{}(Token):".format(Rule[0][1]))
            self.IdentLevel += 1
            self.CurrentVar = Rule[0][1]
            if(self.CurrentVar in self.RulesList):
                print("Rule_{} has already been created".format(self.CurrentVar))
                raise ValueError
            return Rule[2:]
        else:
            raise Exception("Input is flawed in EBNFParserGenerator")
            
    def PrintIndented(self, String):
        print("{}{}".format(self.Indent(),String))

    def Indent(self):
        return " "*self.IdentLevel*4


        
Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"
x = EBNFParserGenerator(Path,GrammarFile)
print(x.Dict_KeyToValue)