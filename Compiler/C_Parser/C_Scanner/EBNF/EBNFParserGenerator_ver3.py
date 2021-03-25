#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:33:07 2021

@author: tim
"""
from EBNFParser_ver2 import EBNFParser

class EBNFParserGenerator():
    
    def __init__(self,Path,GrammarFile):
        self.Position = 0
        self.RuleName = ""
        self.RulePosition = 0
        self.IdentLevel = 0
        self.Start, self.End = 0,0
        self.VarNames = []
        self.EBNF_KeyToValue, self.EBNF_ValueToKey = {}, {}
        self.GrammarStream = []
        self.GetParsedGrammar(Path,GrammarFile)
        self.Length = len(self.GrammarStream)
        self.Rules = self.RulesList()
        self.RulesIntepreter()
        
        
    def GetParsedGrammar(self, Path, GrammarFile):
        TokenList = "EBNFTokenList.txt"
        GrammarParser = EBNFParser(Path,GrammarFile,TokenList)
        self.GrammarStream = GrammarParser.ParsedGrammar
        self.EBNF_KeyToValue =  GrammarParser.Dict_KeyToValue
        self.EBNF_ValueToKey = GrammarParser.Dict_ValueToKey
        
        
    def GetToken(self):
        if(self.Position >= self.Length):
            raise Exception("Length of EBNF is exceeded")
        #print(self.Position)
        Token = self.GrammarStream[self.Position]
        self.Position += 1
        return Token

    def RulesList(self):
        Start, End = 0,0
        RuleStartEnds = []
        RuleCount = 0
        
        for i in range(0,self.Length):
            if(self.GrammarStream[i] == "START RULE"):
                Start = i
                RuleStartEnds.append([Start,0])
                self.VarNames.append(self.GrammarStream[i+1][1])
                
            if(self.GrammarStream[i] == "END RULE"):
                End = i
                RuleStartEnds[RuleCount][1] = End
                RuleCount += 1
                
        return RuleStartEnds
                
    def RulesIntepreter(self):
        for i in self.Rules:
            self.Start, self.End = i[0]+3, i[1]
            self.IdentLevel = 0
            #+3 to skip rule name, assignment operator and so forth
            self.Position = self.Start
            self.RulePosition = 0
            self.RuleName = self.GrammarStream[i[0]+1][1]
            self.Offset = 1
            self.StartRule()
            self.StartMainLoop()
            print("\nEND OF RULE \n")
    
    def StartMainLoop(self):
        x = self.GetToken()
        #print(x)
        if(x == "END RULE"):
            self.IdentLevel += 1
            print("{}Flag_{} = True".format(self.Ident(),self.RulePosition+1))
            self.IdentLevel = 1
            print("{}return Flag_0".format(self.Ident()))
            self.IdentLevel += 1
            return 0
        elif(x[0] == "CONST"):
            self.CheckConst(x)
        elif(x[0] == "OP"):
            self.CheckOp(x)
        elif(x[0] == "VAR"):
            self.CheckVar(x)
        
    
    def CheckConst(self,x):
        print("{}if(Tokens[{}] == {}):".format(self.Ident(),self.RulePosition,x[1]))
        self.StartMainLoop()
        
    def CheckOp(self,x):
        if(x[1] == 9): # 9 is ,
            self.RulePosition += 1
            self.IdentLevel += 1
        if(x[1] == 12): # 12 is |
            self.IdentLevel += 1
            print("{}Flag_{} = True".format(self.Ident(),self.Offset-1))
            self.IdentLevel = self.Offset
        if(x[1] == 2): # 2 is {
            print("{}Flag_{} = True".format(self.Ident(),self.RulePosition+1))
            print("{}while(Flag_{} == True)):".format(self.Ident(),self.RulePosition+1))
            self.IdentLevel += 1
            self.Offset += 2
        if(x[1] == 3): #3 is }
            print("{}Flag_0 = True".format(self.Ident(),self.Offset))
            self.Offset -= 2
            self.IdentLevel -= 1
        
        self.StartMainLoop()
        
    def CheckVar(self,x):
        if(x[1] not in self.VarNames):
            print("################")
            print("################")
            raise Exception("UNDEFINED VARIABLE")
        if(x[1] in self.VarNames):
            print("{}if(Rule_{}(Tokens[{}]) == True):".format(self.Ident(),x[1],self.RulePosition))
            
            
        self.StartMainLoop()
        
    def StartRule(self):
        print("def Rule_{}(Tokens):".format(self.RuleName))
        self.IdentLevel += 1
        print("{}Flag_{} = False".format(self.Ident(),0))

        
    def Ident(self):
        return " "*self.IdentLevel*4
        
Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"

x = EBNFParserGenerator(Path,GrammarFile)
print(x.EBNF_KeyToValue)