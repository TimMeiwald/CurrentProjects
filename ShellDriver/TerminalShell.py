#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:09:34 2021

@author: tim
"""

import ShellDriver3 as SD


class TerminalShell():
    """REPL using Shell Driver.
    
    i.e uses Python terminal of user to act as
    Shell in Read - Evaluate - Print - Loop
    """
    
    def __init__(self, ID):
        self.Driver = SD.ShellDriver(ID)
        self.REPL()
        
    def REPL(self):
        """Read - Evaluate - Print - Loop."""
        while(True):
            WorkingDirectory = self.Driver.Interact("pwd")[0].rstrip()
            print("PyShell: {}: ".format(WorkingDirectory))
            Input = input("")
            if(Input == "exit"):
                self.Driver.Terminate()
                print("Successfully exited")
                break
            Temp = self.Driver.Interact(Input)
            for i in Temp:
                print(i)
        return 0
    
    
x = TerminalShell(0)
