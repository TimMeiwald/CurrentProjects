#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:22:55 2021

@author: tim
"""

from EBNFScanner import Scanner
#from StandardScanner_pipeVer2 import Scanner



from EBNFScanner import Scanner
#from StandardScanner_pipeVer2 import Scanner


class EBNFParser():
    
    def __init__(self,Path,GrammarFile,TokenList):
        self.GrammarFile = []
        self.Dict_KeyToValue, self.Dict_ValueToKey = {},{}
        self.ReadGrammarFile(Path,GrammarFile,TokenList)
        
        self.Letter = self.CreateLetter()
        self.Digit = self.CreateDigit()
        self.Symbol = self.CreateSymbol()
        
        
        self.IndentLevel = 0 #Current Identation value
        self.Position = 0 #
        self.LhsFlag = False # 
        self.IndentOffset = 1
        self.PositionOffset = 0
        self.Grammar(self.GrammarFile)

        
    def ReadGrammarFile(self,Path,GrammarFile,TokenList):
        scanner = Scanner(Path,GrammarFile,TokenList)
        i = b""
        while i != b"EOF":
            i = scanner.GetToken()
            self.GrammarFile.append(i)
        self.Dict_KeyToValue, self.Dict_ValueToKey = scanner.Dict_KeyToValue, scanner.Dict_ValueToKey 
        scanner.CloseFile()
    
    def CreateLetter(self):
        #In ASCII vals
        Letter = []
        #Upper case A-Z
        for i in range(65,91):
            Letter.append(chr(i))
        #Lower case a-z
        for i in range(97,123):
            Letter.append(chr(i))
        return Letter


    def CreateDigit(self):
        Digit = []
        #Digits 0-9
        for i in range(48,58):
            Digit.append(chr(i))
        return Digit
    
    def CreateSymbol(self):
        symbol = []
        #All ASCII symbols
        for i in range(0,255):
            symbol.append(chr(i))
        return symbol
        
    def Character(self,Token):
        if(Token in self.Letter):
            return 0
        elif(Token in self.Digit):
            return 0
        elif(Token in self.Symbol):
            return 0
        elif(Token == "_"):
            return 0
        else:
            print("Character Error 1 with Token {}".format(Token))
            return -1
    
    def Identifier(self,Token):
        if(Token[0] in self.Letter):
            for i in Token[1:]:
                if(i in self.Letter):
                    continue
                elif(i in self.Digit):
                    continue
                elif(i == "_"):
                    continue
                else:
                    return -1
            if(self.LhsFlag == False):
                String = "if(Rule_{}(TokenList[{}]) == 0): ".format(Token,self.Position)
                self.Write(String)
                return 0
            else:
                self.LhsFlag = False
                return 0
        else:
            return -1            
    
    def Terminal(self,Token):
        Chrs = ["'", '"']
        for j in Chrs:
            if(Token[0] == j):
                for i in Token[1:-2]:
                    if(self.Character(i) == 0):
                        continue
                    else:
                        print("Terminal Error 1 with Token {}".format(Token))
                        return -1
                if(Token[-1] == j):
                    String = "if(TokenList[{}] == {}): ".format(self.Position,Token)
                    self.Write(String)
                    return 0
                else: 
                    print("Terminal Error 2 with Token {}".format(Token))
                    return -1
        print("Terminal Error 3 with Token {}".format(Token))
        return -1
            
    
    def Lhs(self,Token):
        self.IndentLevel = 0
        self.Position = 0
        self.Offset = 1
        self.Write("def Rule_{}(TokenList):".format(Token))
        self.IndentLevel += 1
        self.LhsFlag = True
        if(self.Identifier(Token) == 0):
            return 0
        else:
            print("Lhs Error 1 with Token {}".format(Token))
            return -1
        
    def Rhs(self,TokenList):
        if(len(TokenList) == 1):
            TokenList = TokenList[0]
        if(type(TokenList) == str):
            if(self.Identifier(TokenList) == 0):
                return 0
            elif(self.Terminal(TokenList) == 0):
                return 0
        
        ChrsStart = ["[","{","("]
        ChrsEnd = ["]","}",")"]
        for i in range(0,3):
            ChrsStart[i] = self.Dict_KeyToValue[bytes(ChrsStart[i],encoding = "ASCII")]
            ChrsEnd[i] = self.Dict_KeyToValue[bytes(ChrsEnd[i],encoding = "ASCII")]
            
        # | "[" , rhs , "]"
        # Option
        Start = ChrsStart[0]
        End = ChrsEnd[0]
        if(TokenList[0] == Start and TokenList[-1] == End):
            if(self.Rhs(TokenList[1:-1]) == 0):
                return 0
            else:
                print("Rhs Error 1 with Token {}".format(i))
                return -1
            return 0
        
        #| "{" , rhs , "}"
        #Repetition
        Start = ChrsStart[1]
        End = ChrsEnd[1]
        if(TokenList[0] == Start and TokenList[-1] == End):
            self.Write("WHILE LOOP or SOME SHIT")
            self.IndentLevel += 1
            self.IndentOffset = self.IndentLevel 
            self.PositionOffset = self.Position
            if(self.Rhs(TokenList[1:-1]) == 0):
                self.Write("END WHILE LOOP")
                self.IndentOffset = 1
                self.IndentLevel -= 1
                self.PositionOffset = 0
                return 0
            else:
                print("Rhs Error 1 with Token {}".format(i))
                return -1
            return 0
        
        #| "(" , rhs , ")"
        #Grouping
        Start = ChrsStart[2]
        End = ChrsEnd[2]
        if(TokenList[0] == Start and TokenList[-1] == End):
            if(self.Rhs(TokenList[1:-1]) == 0):
                return 0
            else:
                print("Rhs Error 1 with Token {}".format(i))
                return -1
            return 0
        
        Seps = ["|",","]
        for i in range(0,2):
            Seps[i] = self.Dict_KeyToValue[bytes(Seps[i],encoding = "ASCII")]
        
        # rhs , "," , rhs 
        Count = 0
        for j in TokenList:
            if(j == 9):#9 is ,
                Lefthandside_of_Rhs = TokenList[0:Count]
                Righthandside_of_Rhs = TokenList[Count+1:]
                if(self.Rhs(Lefthandside_of_Rhs) == 0):
                    self.Position += 1
                    self.IndentLevel += 1
                    if(self.Rhs(Righthandside_of_Rhs) == 0):
                        return 0
                else:
                    print("Rhs Error 2 with Token {}".format(j))
                    return -1  
            Count += 1
            
        # rhs , "|" , rhs 
        Count = 0
        for j in TokenList:
            if(j == 12): #12 is |
                Lefthandside_of_Rhs = TokenList[0:Count]
                Righthandside_of_Rhs = TokenList[Count+1:]
                if(self.Rhs(Lefthandside_of_Rhs) == 0):
                    self.IndentLevel += 1
                    self.Write("return True")
                    self.IndentLevel = self.IndentOffset
                    self.Position = self.PositionOffset
                    if(self.Rhs(Righthandside_of_Rhs) == 0):
                        return 0
                else:
                    print("Rhs Error 2 with Token {}".format(j))
                    return -1  
            Count += 1
            
            
        print("Rhs Error 3 with Tokens {}".format(TokenList))
        return -1
                        
              
    def Rule(self, TokenList):
        print("\n")
        Chr = self.Dict_KeyToValue[bytes("=",encoding = "ASCII")]
        EndChr = self.Dict_KeyToValue[bytes(";",encoding = "ASCII")]
        if(self.Lhs(TokenList[0]) == 0):
            if(TokenList[1] == Chr):
                if(self.Rhs(TokenList[2:-1]) == 0):
                    if(TokenList[-1] == EndChr):
                        self.IndentLevel += 1
                        self.Write("return True")
                        self.IndentLevel = 1
                        self.Write("return False")
                        return 0
                    else:
                        print("Rule error 1 with {}".format(TokenList))
                        return -1
                else:
                    print("Rule error 2 with {}".format(TokenList))
                    return -1
            else:
                print("Rule error 3 with {}".format(TokenList))
                return -1
        else:
            print("Rule error 4 with {}".format(TokenList))
            return -1
    
    def Grammar(self, TokenList):
        EndChr = self.Dict_KeyToValue[bytes(";",encoding = "ASCII")]
        Count = 0
        Pos = 0
        Rules = []
        for i in TokenList:
            Count += 1
            if(i == EndChr):
                Rules.append(TokenList[Pos:Count])
                Pos = Count
        for i in Rules:
            if(self.Rule(i) == 0):
                pass
            else:
                raise Exception("Grammatical Errors in Rule")
        return "\nGrammar is syntactically correct"
    
    
    def Write(self,String):
        #Writes to output if debug == False else prints output
        debug = True
        if(debug == True):
            print("{}{}".format(self.Indent(),String))
        else:  
             String = "\n{}{}".format(self.Indent(),String)
             self.ResultString += String


    def Indent(self):
        #Uses self.IndentLevel to prepend a tab for each level to output
        return " "*self.IndentLevel*4


Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"
TokenList = "EBNFTokenList.txt"
x = EBNFParser(Path,GrammarFile,TokenList)