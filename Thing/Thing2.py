#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 13:11:04 2021

@author: tim
"""

#Takes in list of lists 

import subprocess as s




proc = s.Popen("pwd",stdin = s.PIPE, stdout = s.PIPE, stderr = s.PIPE)
output = proc.poll()
print(output.e)


x = proc.communicate(b"ls \n")[0]
proc.stdout.read()