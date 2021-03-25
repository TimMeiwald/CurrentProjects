#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:08:38 2021

@author: tim
"""

from EBNFParser_ver2 import EBNFParser

class EBNFParserGenerator():
    
    def __init__(self,Path,GrammarFile):
        self.Flag_OpenList = False
        self.CurrentVar = 0
        self.Position = 0
        self.Start,self.End = 0,0
        self.EBNF_KeyToValue, self.EBNF_ValueToKey = {}, {}
        self.Vars = []
        self.GrammarStream = []
        self.GetParsedGrammar(Path,GrammarFile)
        self.Length = len(self.GrammarStream)
        self.Rules = self.RulesList()
        self.CreateNewRuleFunction(self.Rules[0][0],self.Rules[0][1])
        self.CreateNewRuleFunction(self.Rules[3][0],self.Rules[3][1])
        
        
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
                
            if(self.GrammarStream[i] == "END RULE"):
                End = i
                RuleStartEnds[RuleCount][1] = End
                RuleCount += 1
                
        return RuleStartEnds
                
    
    def CreateNewRuleFunction(self,Start,End):
        Rule = self.GrammarStream[Start+1:End+1]
        self.Position = Start + 1
        x = self.GetToken()
        print("def Rule_{}(Token):\n".format(x[1]))
        #print("    {} = ".format(x[1]))
        Var = x[1]
        x = self.GetToken()
        if(x != ("OP", 11)): #11 is =
            raise Exception("Needs assignment operator")
        self.Start, self.End = Start + 1, End+1
        self.Flag_OpenList = False
        self.MainRuleLoop()
        print("\n \nraise Exception('If it gets here something failed')\n")
        self.Vars.append(Var)
        return 0
        
    def MainRuleLoop(self):
        if(self.Position >= self.End):
            raise Exception("Shouldn't get here")
        x = self.GetToken()
        if(x[0] == "CONST"):
            self.Const(x)
        elif(x[0] == "OP"):
            self.Op(x)
        elif(x[0] == "VAR"):
            self.Var(x)
        elif(x == "END RULE"):
            if(self.Flag_OpenList == True):
                print("]")
                print("if(Token in i_{}): \n return True".format(self.CurrentVar))
                print("else:\n    return False")
            else:
                return 0
        else:
            raise Exception("Should never get here in MainRuleLoop")

        
    def Const(self,Token):
        if(self.Flag_OpenList == False):
            self.CurrentVar += 1
            print("i_{} = ".format(self.CurrentVar))
            print("[")
        self.Flag_OpenList = True
        
        print(Token[1])
        self.MainRuleLoop()
        
    def Op(self,Token):
        if(self.Flag_OpenList == True and Token[1] == 12):
            #12 is |
            print(",")
        elif(self.Flag_OpenList == False and Token[1] == 9):
            pass
        elif(Token[1] != 12):
            print("]")
            print("if(Token in i_{}): \n return True".format(self.CurrentVar))
            print("else:\n    return False")
        self.MainRuleLoop()
        
    def Var(self,Token):
        self.Flag_OpenList = False
        if(Token[1] in self.Vars):
            print("    if(Token in Rule_{}(Token)):\n        return True".format(Token[1]))
        else:
            print("Undefined variable")
        self.MainRuleLoop()

        
Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"

x = EBNFParserGenerator(Path,GrammarFile)
print(x.EBNF_KeyToValue)