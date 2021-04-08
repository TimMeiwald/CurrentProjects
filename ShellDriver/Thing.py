#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 12:09:39 2021
@author: tim
"""

import os 


#SpecialChar $
class Get():

    def __init__(self,TargetString,*ListArgs):
        #File with Grep Notation
        #e.g wildcards *

        self.ListArgsCount = 0
        self.Current = []
        self.DiscreteTargets = []
        self.ListArgs = ListArgs
        self.Destination = Destination
        self.IdentifyTargets(TargetString)

    def IdentifyTargets(self,TargetString):
        Targets = self.SplitbyChar(TargetString,"/")

        for i in range(0,len(Targets),1):
            if(Targets[i][0] == "$"):
                Targets[i] = []
                for j in self.ListArgs[self.ListArgsCount]:
                    Targets[i].append(j)
                self.ListArgsCount += 1
        self.GetFiles(Targets)


    def GetFiles(self,Targets):
        #print(self.Current)
        if(Targets == []):
            self.DiscreteTargets.append(self.Current)
            self.Current = []
            return 0 
        Type = type(Targets[0])
        Vals = Targets[0]
        if(Type == str):
            self.Current += [Vals]
            self.GetFiles(Targets[1:])

        if(Type == list):
            Node = self.Current
            for j in Vals:
                self.Current = Node + [j]
                self.GetFiles(Targets[1:])




    def SplitbyChar(self,String, Char):
        #Splits a string by the char(discards the char)
        #e.g SplitbyChar(/home/Documents,/)
        #Would return [home,Documents]
        Start, End = 0, 0
        SubStringList = []
        for i in String:
            if(i == Char):
                SubString = String[Start+1:End]
                if(SubString != ""):
                    SubStringList.append(SubString)
                Start = End
            End += 1
        if(String[End-1] == Char):
            raise Exception(""" Must end with a file location and not with '/'. 
                If you wish to copy the entire directory use 
                the wildcard '*' to terminate the string""")
        SubStringList.append(String[Start+1:End])
        return SubStringList


Targets = "/home/blah/Documents/*/$/There/Are/$"
Destination = "/home/tim/Documents/PapasCode2/"
def UnitTest(Targets,Destination):
    RandList1 = ["Apples","Bananas","Pears"]
    RandList2 = ["Cars","Mustangs"]
    RandList3 = ["Horses","Bears"]
    x = Get(Targets,RandList1,RandList2,RandList3)
    print(x.DiscreteTargets)
    return x

x = UnitTest(Targets,Destination) 