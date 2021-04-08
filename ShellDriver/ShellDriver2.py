#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 17:30:42 2021

@author: tim
"""

from subprocess import Popen, PIPE, STDOUT
import threading
import time


class ShellDriver():
    """Class to control shell as if you were manually using a terminal.
    
    Allows an intuitive programmatic interface to interactively use a
    "terminal"
    """
    
    def __init__(self, ID):
        self.KILL = False
        self.output = []
        self.process = Popen(["/bin/bash"], stdin=PIPE, stderr=STDOUT,
                             stdout=PIPE, text=True, bufsize=1)
        self.ReadThread = threading.Thread(target=self.NonBlockingRead)
        self.ReadThread.start()

    def NonBlockingRead(self):
        """Abuses OS, when it's blocked control is passed back to main."""
        while(True):
            Temp = self.process.stdout.readline().rstrip()
            self.output.append(Temp)
            if(self.KILL):  # self.KILL == True when Terminate is called
                return 0
            
    def Read(self):
        """Return everything currently in output and then empties it."""
        Temp = self.output
        self.output = []
        return Temp

    def Write(self, Input):
        """By sleeping control handed to ReadThread(since Python has GIL."""
        self.process.stdin.write(Input + "\n")
        time.sleep(1)
        
    def Terminate(self):
        """End readThread, ends Popen process."""
        self.KILL = True
        self.Write("exit")  # Closes the pipe, allowing read thread to end
        self.ReadThread.join()
        self.process.terminate()
        

Driver = ShellDriver(0)

Driver.Write(("ls"))
x = Driver.Read()
print(x)
Driver.Write(("cd ../"))
x = Driver.Read()
print(x)
Driver.Write("ls")
x = Driver.Read()
print(x)
Driver.Write("pwd")
x = Driver.Read()
print(x)

Driver.Terminate()
