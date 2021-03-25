#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 16:00:01 2021

@author: tim
"""

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep


class BrowserNavigator():
    
    def __init__(self):
        self.currentURL = ""
        try:    
            self.browser = Firefox()
        except:
            raise Exception(""" For some reason Selenium Firefox driver failed 
            Check for updates that may have broken the code 
            Check that Geckodriver is in PATH and installed""")

    def navigateToURL(self,URL):
        if(URL == ""):
            raise Exception("You need to provide a URL")            
        try:
            self.browser.get(URL)
            self.currentURL = URL
        except:
            raise Exception(""" Failed to go to that URL, Check you gave valid URL
            Check Wifi and Internet connection""")
    
    def CloseBrowser(self):
        self.browser.close()
        
        
class GoogleNavigator(BrowserNavigator):
    def __init__(self):
        BrowserNavigator.__init__(self)
        BrowserNavigator.navigateToURL(self,"https://Google.co.uk")
        
        #Deal with terms and conditions popup/iframe
        try:
            #Switches to iframe of pop up
            self.browser.switch_to.frame(self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/span/div/div/iframe'))
            #Finds I agree button and clicks
            self.browser.find_element_by_id("introAgreeButton").click()
            #returns to default content
            self.browser.switch_to.default_content()
        except:
            raise Exception("Dealing with Googles terms and conditions pop up failed, check if xpath is still correct")
            self.browser.close()


        
        
        