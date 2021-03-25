#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 12:23:24 2021

@author: tim
"""
from EBNFParser_ver2 import EBNFParser


class EBNFParserGenerator():
    
    def __init__(self,Path,GrammarFile):
        self.IndentLevel, self.Offset, self.PositionOffset = 0, 0, 1
        self.Temp = ""
        self.ResultString = ""
        self.RulesList = []
        self.fileHandler =  self.OpenFile(Path, "ParsedGrammar.py")
        self.x = self.GetParsedGrammar(Path,GrammarFile)
        self.Tokenstream = self.x[0]
        TokenStream = self.x[0]
        self.Dict_KeyToValue = self.x[1]
        self.Dict_ValueToKey = self.x[2]
        Rules = self.SplitRules(TokenStream)
        Rules = self.ParseRules(Rules)
        self.CloseFile()
    
    def OpenFile(self,Path,File):
        try:
            fileHandler = open(Path + File, "w")
            return fileHandler
        except:
            raise Exception("Failed to open file, check path and file")
    
    def CloseFile(self):
        try:
            self.fileHandler.close()
            return 0
        except:
            raise Exception("Could not successfully close file")
        
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
                self.IdentLevel, self.Offset,self.PositionOffset = 0, 0, 1
                self.EndString = "return True"
                self.ResultString = ""
                self.ParseRule(Rules[i])
                self.RulesList.append(self.CurrentVar)
                print("Successfully created rule: {}".format(self.CurrentVar))
                TrueCount += 1
                self.fileHandler.write(self.ResultString)
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
        self.WriteToResultStringIndented("if(TokenList[{}] == {}):".format(self.IdentLevel-self.PositionOffset,TokenVal))
        
    def Ops(self,TokenVal):
        #print(self.Offset, self.IdentLevel)
        if(TokenVal == 12): #12 is | or OR
            # Returns to function level indentation on or, unless offset has
            #been modified by e.g {} which indicates a repetition aka for loop
            self.IdentLevel += 1
            self.WriteToResultStringIndented("{}".format(self.EndString))
            self.IdentLevel -= 1
            self.IdentLevel = self.Offset +1
        if(TokenVal == 9): #9 is , which is concat
            # if , then it means first token followed by second token etc
            #so by changing Identlevel we schain the if statements
            self.IdentLevel += 1
        if(TokenVal == 6): #6 is ;, aka end of statement
            if(self.Temp != 3 and TokenVal == 6):
                 self.IdentLevel += 1
                 self.WriteToResultStringIndented("{}".format(self.EndString))
                 self.IdentLevel = 1
                 self.WriteToResultStringIndented("return False")
            else:
                 self.IdentLevel += 1
                 self.WriteToResultStringIndented("Flag = True \n{}continue".format(self.Indent()))

                 
                 self.IdentLevel = 1
                 self.WriteToResultStringIndented("return False".format(self.EndString))
                 
        if(TokenVal == 2): #2 is { opening repetition
            self.PositionOffset += 1
            self.WriteToResultStringIndented("Flag = True")
            self.WriteToResultStringIndented("while(Flag == True):".format(self.IdentLevel-self.PositionOffset))
            self.Offset = self.IdentLevel 
            self.IdentLevel += 1
            self.WriteToResultStringIndented("Flag = False")
            self.EndString = "Flag = True \n{}    continue".format(self.Indent())

        if(TokenVal == 3): #3 is } closing repetition 
            self.WriteToResultStringIndented("Flag = True")
            self.EndString = "return True"
            self.IdentLevel -= 2
            self.PositionOffset = 1
            self.Offset = 0
        self.Temp = TokenVal
        #need to do [] and other stuff in ISO/IEC 14977
            
            
            
    def Vars(self,TokenVal):
        if(TokenVal not in self.RulesList and TokenVal != self.CurrentVar):
            print("Undefined Variable: '{}' in Rule_{}".format(TokenVal,self.CurrentVar))
            raise ValueError("Undefined Variable")
            
        self.WriteToResultStringIndented("if(Rule_{}(TokenList[{}]) == True):".format(TokenVal,self.IdentLevel-self.PositionOffset))
    
    def Tokens(self,Token):
        #print("IdentLevel", self.IdentLevel)
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
        self.CurrentVar = ""
        if(Rule[0][0] == "VAR" and Rule[1][0] == "OP" and Rule[1][1] == 11):
            
            self.CurrentVar = Rule[0][1]
            if(self.CurrentVar in self.RulesList):
                print("Rule_{} has already been created".format(self.CurrentVar))
                raise ValueError
            self.WriteToResultStringIndented("\ndef Rule_{}(TokenList):".format(Rule[0][1]))
            self.IdentLevel += 1
            return Rule[2:]
        else:
            raise Exception("Input is flawed in EBNFParserGenerator")
            
    def PrintIndented(self, String):
        print("{}{}".format(self.Indent(),String))
        
    def WriteToResultStringIndented(self,String):
        debug = True
        if(debug == True):
            print("{}{}".format(self.Indent(),String))
        else:  
             String = "\n{}{}".format(self.Indent(),String)
             self.ResultString += String


    def Indent(self):
        return " "*self.IdentLevel*4


        
Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"
x = EBNFParserGenerator(Path,GrammarFile)
