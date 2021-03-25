#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 12:05:13 2021

@author: tim
"""

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import numpy as np

class BrowserNavigator():
    
    def __init__(self):
        self.currentURL = ""
        try:    
            self.profile = webdriver.FirefoxProfile()
            self.profile.set_preference("browser.download.folderList", 2)
            self.profile.set_preference("browser.download.manager.showWhenStarting", False)
            self.profile.set_preference("browser.download.dir", "/home/tim/Documents/Python Scripts/FTSE100StockData")
            self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
            
            self.browser = Firefox(self.profile)
            uBlockOriginLocation = "/home/tim/.mozilla/firefox/iyvhrs0h.default-release/extensions/uBlock0@raymondhill.net.xpi"
            self.browser.install_addon(uBlockOriginLocation,temporary = True)
            #driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
            self.browser.implicitly_wait(10)
            #HARDCODED SLEEP BAD BUT HACK FOR NOW

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
    def randWait(self,MaxLength):
        #human reaction time
        sleep(0.1)
        wait = np.random.random(1)[0]*MaxLength
        sleep(wait)
        
    def CloseBrowser(self):
        self.browser.close()
        
        
class NavigateYahooFinance(BrowserNavigator):
    def __init__(self):
        BrowserNavigator.__init__(self)
        BrowserNavigator.navigateToURL(self,"https://finance.yahoo.com")
        
        #Deal with terms and conditions popup/iframe
        try:
            sleep(2)
            self.browser.find_element_by_name("agree").click()
            #HARDCODED SLEEP BAD BUT HACK FOR NOW
        except:
            raise Exception("Dealing with Yahoos terms and conditions pop up failed, check if element name is still correct")
            self.browser.close()


    def useYahooSearchBar(self,Input):
        #Current Name of Yahoo search bar
        name="yfin-usr-qry"
        #Needs [0] for reasons that I don't understand unfortunately
        self.randWait(0.5)
        try:
            searchBar = self.browser.find_elements_by_name(name)[0]
        except:
            raise Exception("Failed to find Yahoo Search bar, check if html name has changed")
        print(searchBar)
        for i in Input:
            searchBar.send_keys(i)
            self.randWait(0.1)
        #searchBar.send_keys(Input)
        sleep(0.5)
        self.randWait(0.3)
        #Keeps going to same page for some reason without the long delays bizarrely
        #self.browser.find_elements_by_id("search-buttons").click()
        searchBar.send_keys(Keys.RETURN)

    def clickHistoricalDataButton(self):
        try:
            self.browser.find_elements_by_css_selector('li.IbBox:nth-child(5)')[0].click()
            #y = self.browser.find_elements_by_css_selector(css_selector).click()
        except:
            raise Exception("Failed to click historical data button, check if xpath has changed")

    def DownloadLastMonthsDataCSV(self):
        try:
            css_selector = "a.Fl\(end\):nth-child(1)"
            self.browser.find_elements_by_css_selector(css_selector)[0].click()
        except:
            raise Exception("DownloadLastMonthsDataCSV failed")



class webscraperFTSE100HistoricalDaily(NavigateYahooFinance):
    
    def __init__(self):
        self.FTSE100List = np.genfromtxt('AuxiliaryCSVFiles/FTSE100Names.csv',delimiter = "'",dtype = str)
        NavigateYahooFinance.__init__(self)
        self.scrapeFTSE100Data()
        
    def scrapeFTSE100Data(self):
        LondonStockExchanceID = ".L"
        FailureCounter = 0
        for i in np.arange(0,101,1):
            if(FailureCounter >= 3):
                raise Exception("Multiple failures of same ticker, check everything")
            try:
                Ticker = self.FTSE100List[i] + LondonStockExchanceID
                try:
                    self.useYahooSearchBar(Ticker)
                    self.randWait(3)
                    sleep(2)
                except:
                    raise Exception("Failed to get {}".format(Ticker))
                try:
                    self.clickHistoricalDataButton()
                    sleep(3)
                    self.randWait(5)
                except: 
                    raise Exception("clickHistoricalDataButton failed for {}".format(Ticker))
                try:
                    self.DownloadLastMonthsDataCSV()
                    sleep(5)
                    self.randWait(5)
                    print("{} successfully downloaded".format(Ticker))
                except:
                    raise Exception("DownloadLastMonthsDataCSV for {} failed".format(Ticker))
                FailureCounter = 0
            except:
                #Will try again after 5 secconds, increments a counter to terminate
                #if same ticker attempted more than 3 times. 
                i -= 1
                FailureCounter += 1
                sleep(5)
            
                #raise Exception("DownloadLastMonthsDataCSV failed for {}".format(Ticker))
        self.browser.close()



#sorta works but sometimes breaks due to wifi issues, going to build more robust version in
# SeleniumTest5



