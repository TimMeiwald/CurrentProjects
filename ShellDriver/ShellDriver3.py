#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 19:31:08 2021

@author: tim
"""

from subprocess import Popen, PIPE, STDOUT
import threading
import time
import queue


class ShellDriver():
    """Class to control shell as if you were manually using a terminal.
    
    Allows an intuitive programmatic interface to interactively use a
    "terminal"
    """
    
    def __init__(self, ID):
        self.KILL = False
        self.output = []
        self.queue = queue.SimpleQueue()
        self.process = Popen(["/bin/bash"], stdin=PIPE, stderr=STDOUT,
                             stdout=PIPE, text=True, bufsize=1)
        self.ReadThread = threading.Thread(target=self.NonBlockingRead)
        self.ReadThread.start()

    def NonBlockingRead(self):
        """Abuses OS, when it's blocked control is passed back to main."""
        while(True):
            self.queue.put(self.process.stdout.readline().rstrip())
            if(self.KILL):  # self.KILL == True when Terminate is called
                return 0
            
    def Read(self):
        """Return everything currently in output queue."""
        Temp = []
        while(self.queue.empty() is not True):
            Temp.append(self.queue.get())
        return Temp

    def Write(self, Input):
        """By sleeping control handed to ReadThread(since Python has GIL."""
        self.process.stdin.write(Input + "\n")
        time.sleep(0.01)  # Allows blocking read thread to take control again
        
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
