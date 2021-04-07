#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:35:00 2021

@author: tim
"""

import Utils as U
# Grammar consists of sequence of rules of the form
# rule_name: expression
# or optionally
# rule_name[return_type]: expression
# Should follow PEP617 notation, possibly only subset


class PEG():
    
    def __init__(self,filePath):
        self.grammar = U.ReadTextFile(filePath)
        self.KnownRules = {}
        #print(self.grammar)
        self.Grammar()
    
    def evalExpression(self,expression):
        ruleType = U.NextSpecialChar(expression)
        # print("{}: {}".format(ruleType,expression))
        eval("self." + ruleType + "('{}')".format(expression))
        return 0  
    
    def Terminal(self,expression):
        if(expression == ""):
            return 0
        else:
            NewRule = U.SearchForRule(self.grammar, expression+":")
            if(NewRule == "No Rule"):
                # print("TERMINAL: {}".format(expression))
                return 0
            self.Rule(NewRule)
            return 0
    
    def Grammar(self):
        """Grammar consists of sequence of rules, 
        with a defined starting rule.
        Current hardcoded starting rule 'start'"""
        startingRule = U.SearchForRule(self.grammar,"start:")
        self.Rule(startingRule)
    
    def Rule(self,rule):
        """Exact pattern required 'rule_name: expression' ."""
        name, expression = U.SplitByString(rule,":")
        if(name in self.KnownRules):
            # print("VAR: {}".format(rule) )
            return 0
        self.KnownRules[name] = expression
        self.evalExpression(expression)
       
        
    def Comment(self):
        """# style comments"""
        pass
    
    def Sequence(self,expression):
        """Split sequence and then evaluate both new expressions"""
        expr1, expr2 = U.SplitByString(expression," ")
        Result1 = self.evalExpression(expr1)
        Result2 = self.evalExpression(expr2)
        if(Result1 == 0 and Result2 == 0):
            # print("Sequence")
            return 0
        else:
            return -1
    
    def OrderedChoice(self,expression):
        """Check whether either sequence returns true in order then evaluate"""
        expr1, expr2 = U.SplitByString(expression, "|")
        
        Result = self.evalExpression(expr1)
        self.evalExpression(expr2)
        if(Result == 0):
            # print("Choice 1")
            return Result
        elif(self.evalExpression(expr2) == 0):
            #print("Choice 2")
            return self.evalExpression(expr2)
        
    def ZeroOrMore(self,expression):
        expr1, expr2 = U.SplitByString(expression,"*")
        # print("ZEROORMORE:",expr1)
        self.evalExpression(expr1)
        self.evalExpression(expr2)
    
    def OneOrMore(self,expression):
        expr1, expr2 = U.SplitByString(expression,"+")
        # print("One or More: {}".format(expression))
        self.evalExpression(expr1)
        self.evalExpression(expr2)
    
    
    def Optional(self,expression):
        expr1, expr2 = U.SplitByString(expression[1:],"]")
        Result1 = self.evalExpression(expr1)
        Result2 = self.evalExpression(expr2)
        if(Result1 == 0):
            return Result1
        elif(Result2 == 0):
            return Result2
        else:
            return -1
    
    def AndPredicate(self):
        # Succeed if e can be parsed, without consuming any input.
        pass
    
    
    def NotPredicate(self):
        #Fail if e can be parsed, without consuming any input.
        pass
    
    def Instruction(self,expression):
        expr1, expr2 = U.SplitByString(expression[1:],"}")
        print(expr1)
    
class PEG_Test():
    
    def __init__(self):
        filePath = "/home/tim/Documents/CurrentProjects/Compiler/C_Parser/C_Scanner/PEG/PEGTestFile.txt"
        pEG = PEG(filePath)
        print(pEG.KnownRules)
    


Test = PEG_Test()