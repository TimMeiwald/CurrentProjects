#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:48:53 2021

@author: tim
"""
import Utilities

class Tokens():  
    
    def __init__(self,Path,File):
        self.Reserved = ["EOL",
                        "OPEN",
                        "CLOSE",
                        "INDENT",
                        "STRINGS",
                        "COMMENTS",
                        "MULTILINECOMMENTS",
                        "KEYWORDS",
                        "OPERATORS",
                        "TERMINATION"]
        self.Position = 0
        self.TokenList = Utilities.readFileToString(Path,File).split()
        self.TokenListLength = len(self.TokenList)
        self.EOL = self.getEOL()
        self.Indent = self.getStringsOrCommentsOrMultiLineCommentsOrIndent("INDENT")
        self.Strings = self.getStringsOrCommentsOrMultiLineCommentsOrIndent("STRINGS")
        self.Comments = self.getStringsOrCommentsOrMultiLineCommentsOrIndent("COMMENTS")
        self.MultiLineComments = self.getStringsOrCommentsOrMultiLineCommentsOrIndent("MULTILINECOMMENTS")
        self.Keywords = self.getKeywordsOrOperators("KEYWORDS")
        self.Operators = self.getKeywordsOrOperators("OPERATORS")
        
    
    def getEOL(self):
        for i in range(self.Position,self.TokenListLength):
            if(self.TokenList[i] == "EOL"):
                if(self.TokenList[i+1] not in self.Reserved):
                    EOL = self.TokenList[i+1]
                    self.Position += i + 2
                    return EOL
                else:
                    raise Exception("Failed to get valid arguments for EOL")
      
    def getStringsOrCommentsOrMultiLineCommentsOrIndent(self,String):
        for i in range(self.Position,self.TokenListLength):
            if(self.TokenList[i] == String and self.TokenList[i+1] == "OPEN"):
                self.Position += 1
                OpenList = self.getUntilNextReserved()
                CloseList = self.getUntilNextReserved()
                return OpenList, CloseList
            else:
                raise Exception("Failed to get valid arguments for STRINGS")

    def getKeywordsOrOperators(self,String):
        for i in range(self.Position,self.TokenListLength):
            if(self.TokenList[i] == String):
                TokenSubList = self.getUntilNextReserved()
                return TokenSubList
                

    def getUntilNextReserved(self):
        TokenSubList = []
        for i in range(self.Position+1,self.TokenListLength):
            if(self.TokenList[i] in self.Reserved):
                if(TokenSubList == []):
                    raise Exception("Failed to add valid arguments for {}".format(self.TokenList[self.Position]))
                self.Position = i
                return TokenSubList
            else: 
                 TokenSubList.append(self.TokenList[i])
    
    def TokenDict(self):
        TokenDict = {}
        TokenDict["EOL"] = self.EOL
        TokenDict["INDENT"] = self.Indent
        TokenDict["STRINGS"] = self.Strings
        TokenDict["COMMENTS"] = self.Comments
        TokenDict["MULTILINECOMMENTS"] = self.MultiLineComments
        TokenDict["OPERATORS"] = self.Operators
        TokenDict["KEYWORDS"]= self.Keywords
        return TokenDict
        
        

            
  
        
Path = "/home/tim/Documents/Python Scripts/C_Compiler/C_Parser/C_Scanner/"
TokenFile = "Tokens.t"
x = Tokens(Path,TokenFile).TokenDict()
