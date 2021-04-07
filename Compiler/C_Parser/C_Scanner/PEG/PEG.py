#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:01:35 2021

@author: tim
"""

#PEG Grammar
#Finite set N of nonterminal symbols
#Finite set Sigma of terminal symbols disjoint from N
#A finite set P of parsing rules
#An expression e_s termed the starting expression

#Each parsing rule has the form A<-e where A is nonterminal
#and e is a parsing expression

#A parsing expression is a hierarchical expression
#similar to a regular expression which is constructed
#in the following fashion

#1. An atomic parsing expression consists of
#Any terminal symbol
#Any nonterminal symbol, or
# the empty string epsilon

#2. Given any existing parsing expressions e, e1 and e2
# a new parsing expression can be constructed using the
# following operators

# Sequence e1 e2
#Ordered Choice e1 /e2
#Zero or more e*
#One or more e+
#Optional e?
#And predicate: &e
#Not predicate: !e