#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 14:26:51 2021

@author: tim
"""

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
        self.ParsedGrammar = []
        
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
                    #print("Identifier Error 1 with Token {}".format(Token))
                    return -1
            #print("Identifier Success with Token {}".format(Token))
            print("VAR  : {}".format(Token))
            self.ParsedGrammar.append(("VAR",Token))
            return 0
        else:
            #print("Identifier Error 2 with Token {}".format(Token))
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
                    print("CONST: {}".format(Token))
                    self.ParsedGrammar.append(("CONST",Token))
                    return 0
                else: 
                    print("Terminal Error 2 with Token {}".format(Token))
                    return -1
        print("Terminal Error 3 with Token {}".format(Token))
        return -1
            
    
    def Lhs(self,Token):
        if(self.Identifier(Token) == 0):
            #print("VAR: {}".format(Token))
            return 0
        else:
            print("Lhs Error 1 with Token {}".format(Token))
            return -1
        
    def Rhs(self,TokenList):
        #Terminal and Identfier
        if(len(TokenList) == 1):
            TokenList = TokenList[0]
        if(type(TokenList) == str):
            if(self.Identifier(TokenList) == 0):
                #print("Rhs passed into Identifier")
                return 0
            elif(self.Terminal(TokenList) == 0):
                #print("Rhs passed into Terminal")
                return 0
        
        ChrsStart = ["[","{","("]
        ChrsEnd = ["]","}",")"]
        for i in range(0,3):
            ChrsStart[i] = self.Dict_KeyToValue[bytes(ChrsStart[i],encoding = "ASCII")]
            ChrsEnd[i] = self.Dict_KeyToValue[bytes(ChrsEnd[i],encoding = "ASCII")]
            
        # | "[" , rhs , "]"
        #| "{" , rhs , "}"
        #| "(" , rhs , ")"

        for i in range(0,3):
            Start = ChrsStart[i]
            End = ChrsEnd[i]
            if(TokenList[0] == Start and TokenList[-1] == End):
                print("OP   : {}".format(Start))
                self.ParsedGrammar.append(("OP",Start))
              
                if(self.Rhs(TokenList[1:-1]) == 0):
                    print("OP   : {}".format(End))
                    self.ParsedGrammar.append(("OP",End))
                    return 0
                else:
                    print("Rhs Error 1 with Token {}".format(i))
                    return -1
              

                return 0
        
        #| rhs , "|" , rhs
        #| rhs , "," , rhs 
        Seps = ["|",","]
        for i in range(0,2):
            Seps[i] = self.Dict_KeyToValue[bytes(Seps[i],encoding = "ASCII")]
        
        #Ok following works if only | or ,. Not when mixed
        """
        for i in Seps:
            Count = 0
            for j in TokenList:
                if(j == i):
                    print(TokenList[Count+1:])
                    if(self.Rhs(TokenList[0:Count]) == 0):
                        if(self.Rhs(TokenList[Count+1:]) == 0):
                            print("Success for Rhs with Token {}".format(j))
                            return 0
                        else:
                            print("Rhs Error 2 with Token {}".format(j))
                            return -1
                    else:
                        print("Rhs Error 3 with Token {}".format(j))
                        return -1
                Count +=1
        """
        Count = 0
        for j in TokenList:
            if(j in Seps):
                Lefthandside_of_Rhs = TokenList[0:Count]
                Righthandside_of_Rhs = TokenList[Count+1:]
                #print(TokenList[0:Count],TokenList[Count+1:])
               
                if(self.Rhs(Lefthandside_of_Rhs) == 0):
                    print("OP   : {}".format(j))
                    self.ParsedGrammar.append(("OP",j))
                    if(self.Rhs(Righthandside_of_Rhs) == 0):
                        return 0
                else:
                    print("Rhs Error 2 with Token {}".format(j))
                    return -1
                
                
            Count += 1
        print("Rhs Error 3 with Tokens {}".format(TokenList))
        return -1
                        
              
    def Rule(self, TokenList):
        Chr = self.Dict_KeyToValue[bytes("=",encoding = "ASCII")]
        EndChr = self.Dict_KeyToValue[bytes(";",encoding = "ASCII")]
        print("START RULE")
        self.ParsedGrammar.append("START RULE")
        if(self.Lhs(TokenList[0]) == 0):
            #print("VAR: ",TokenList[0])
            if(TokenList[1] == Chr):
                print("OP   : =")
                self.ParsedGrammar.append(("OP",self.Dict_KeyToValue[b"="]))
                if(self.Rhs(TokenList[2:-1]) == 0):
                    if(TokenList[-1] == EndChr):
                        self.ParsedGrammar.append(("OP",TokenList[-1]))
                        print("END RULE \n")
                        self.ParsedGrammar.append("END RULE")
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
                #print("RULE:")
                pass
                #print("Success for Rule \n {} \n".format(i))
            else:
                #print("Grammatical Errors in Rule \n {} \n".format(i))
                raise Exception("Grammatical Errors in Rule")
        return "\nGrammar is syntactically correct"

Path = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/EBNF/"
GrammarFile = "EBNFTest.txt"
TokenList = "EBNFTokenList.txt"
x = EBNFParser(Path,GrammarFile,TokenList)
#y = x.GrammarFile
#print(x.Rule(x.GrammarFile[0:106]))
#print(x.Grammar(x.GrammarFile))
#x.Rhs(['letter', 9, 2, 'letter', 12, 'digit', 12, '"_"', 3])