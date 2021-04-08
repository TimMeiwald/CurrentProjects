#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 13:11:04 2021

@author: tim
"""


from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import threading
import time 


def NonBlockingRead(Driver):
    while(Driver.poll() == None):
        print(Driver.stdout.readline())
        pass

proc = Popen(["/bin/bash"], stdin = PIPE, stderr = STDOUT, stdout = PIPE, text = True, bufsize = 1)
proc.stdin.write("ls\n")
proc.stdin.write("cd ../\n")
proc.stdin.write("ls\n")
#proc.stdin.write("python3 HelloWorld.py\n")


x = threading.Thread(target = NonBlockingRead, args = [proc], daemon = True)
x.start()


