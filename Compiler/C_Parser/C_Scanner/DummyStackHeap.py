#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:07:32 2021

@author: tim
"""

class Stack():
    #Dummy Stack
    def __init__(self,StackName):
        #Since [] is implemented as linked list probably(takes all types)
        self.Stack = []
        self.StackName = StackName
        
    def Push(self,Object):
        self.Stack.append(Object)
    
    def Get(self):
        Temp = self.Stack[-1] #Get most recent value
        del self.Stack[-1]
        return Temp

    
class Heap():
    #Dummy Heap
    def __init__(self,HeapName):
        self.Heap = {}
        self.HeapName = HeapName
        
    def Push(self,ObjectName,Object):
        #Note if ObjectName already exists, the Object assigned will be modified in place
        self.Heap[ObjectName] = Object
        
    def Delete(self,ObjectName):
        del self.Heap[ObjectName] 
    
    def Read(self,ObjectName):
        return self.Heap[ObjectName]


    
"""  
x = Stack(b"Thread1")
x.Push(5)
print(x.Stack)
x.Push("String")
print(x.Stack)
x.Get()
print(x.Stack)

y = Heap(b"Heap1")
a = y.Push(b"a",5)
print(y.Heap)
y.Push(b"b","String")
print(y.Heap)
y.Push(b"b", 7)
y.Read(b"a")
print(y.Heap)
y.Read(b"b")
print(y.Heap)
y.Delete(b"a")
print(y.Heap)
y.Delete(b"b")
print(y.Heap)
"""