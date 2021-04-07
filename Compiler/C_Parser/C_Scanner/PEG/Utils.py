#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:48:43 2021

@author: tim
"""


def ReadTextFile(filePath):
    """Read Text file."""
    with open(filePath) as fileHandle:
        Text = fileHandle.read()
    return Text


def SearchForRule(Text, String):
    """Return first matching Rule with name String in text."""
    Length = len(String)
    TempString = ""
    Position = 0
    for i in Text:
        TempString += i
        if(String == TempString):
            # Get rest of line
            TempString += GetLine(Text[Position+1:])
            return TempString
        if(len(TempString) == Length):
            TempString = TempString[1:]
        Position += 1
    return "No Rule"


def GetLine(Text):
    """Return all text to next newline."""
    TempString = ""
    for i in Text:
        if(i == "\n"):
            return TempString
        TempString += i
    return Exception("GetLine could not find another '\n'")


def SplitByString(Text,String):
    """Return two strings, the string before and after 'String'
    i.e Text = String1+String+String2, Stripping white space, Ignoring "" or '' """
    Length = len(String)
    TempString = ""
    Position = 0
    for i in Text:
        TempString += i
        if(String == TempString):
            String1 = Text[:Position-Length+1].strip(" ")
            String2 = Text[Position+1:].strip(" ")
            return String1, String2
        if(len(TempString) == Length):
            TempString = TempString[1:]
        Position += 1
    return -1
    
    
    
def NextSpecialChar(String):
    """Returns the PEG meaning of the next special char ' ' for sequence
    '/' for ordered choice etc"""
    TempString = ""
    Flag1_StringLiteral, Flag2_StringLiteral = False, False
    EitherOrFlag = False
    Whitespace = 0
    for i in String:
        TempString += i
        if(i == "'"):
            if(Flag1_StringLiteral):
                Flag1_StringLiteral = False
            else:
                Flag1_StringLiteral = True
        if(i == '"'):
            if(Flag2_StringLiteral):
                Flag2_StringLiteral = False
            else:
                Flag2_StringLiteral = True
        EitherOrFlag = Flag1_StringLiteral or Flag2_StringLiteral
        if(i == ":" and EitherOrFlag == False):
            return "Rule"
        if(i == " " and EitherOrFlag == False):
            Whitespace += 1
        if(i == "|" and EitherOrFlag == False):
            return "OrderedChoice"
        if(i == "#" and EitherOrFlag == False):
            return "Comment"
        if(i == "*" and EitherOrFlag == False):
            return "ZeroOrMore"
        if(i == "+" and EitherOrFlag == False):
            return "OneOrMore"
        if(i == "[" and EitherOrFlag == False):
            return "Optional"
        if(i == "&" and EitherOrFlag == False):
            return "AndPredicate"
        if(i == "!" and EitherOrFlag == False):
            return "NotPredicate"
        if(Whitespace == 1):
            return "Sequence"
   
    return "Terminal"