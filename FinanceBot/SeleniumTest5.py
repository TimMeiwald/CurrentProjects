#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:08:38 2021

@author: tim
"""

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
import FileUtilities
class BrowserNavigator():
    
    def __init__(self):
        self.currentURL = ""
        try:    
            
            
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", "/home/tim/Documents/Python Scripts/FTSE100StockData")
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
            
            
            self.browser = Firefox(profile)
            uBlockOriginLocation = "/home/tim/.mozilla/firefox/iyvhrs0h.default-release/extensions/uBlock0@raymondhill.net.xpi"
            self.browser.install_addon(uBlockOriginLocation,temporary = True)
            #driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
            self.browser.implicitly_wait(10)

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
        sleep(4)
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
        try: 
            self.path = "/home/tim/Documents/Python Scripts/FTSE100StockData"
            self.FTSE100StockDataDir = FileUtilities.fileUtilities(self.path)
            self.FTSE100List = np.genfromtxt('AuxiliaryCSVFiles/FTSE100Names.csv',delimiter = "'",dtype = str)
            NavigateYahooFinance.__init__(self)
            self.scrapeFTSE100Data()
        except:
            raise Exception("A problem has occurred when scraping financial data")
        finally:            
            self.browser.close()
        
    def downloadOneFTSE100DataFile(self,Ticker):
        #Purpose download one file
        #Point is an atomic download, and to repeat if failed
        try:
            self.useYahooSearchBar(Ticker)
            self.randWait(3)
            sleep(1)
        
       
            self.clickHistoricalDataButton()
            sleep(1)
            self.randWait(5)

            self.DownloadLastMonthsDataCSV()
            sleep(3)
            self.randWait(5)
            print("Stock: {} successfully downloaded".format(Ticker))
            return True
        except:
            try:
                #Tries to delete the file if it for some reason downloaded but
                #function still failed, to keep it atomic as much as possible
                self.FTSE100StockDataDir.deleteFileInDir(Ticker,".csv")
            except:
                pass
            finally:
                print("Download of {} failed".format(Ticker))
                sleep(3)

        
    def scrapeFTSE100Data(self):
        LondonStockExchangeID = ".L"
        
        
        #Delete all files in dir to ensure data is fresh or obvious failure(no stale data)
        self.FTSE100StockDataDir.deleteAllFilesInDir(self.path)
        DataToBeExtracted = [""]*len(self.FTSE100List)
        Count = 0
        for i in self.FTSE100List:
            DataToBeExtracted[Count] = i + LondonStockExchangeID
            Count += 1
        while(len(DataToBeExtracted) != 0):
            Ticker = DataToBeExtracted[0] 
            if(self.downloadOneFTSE100DataFile(Ticker) == True):
                DataToBeExtracted.remove(Ticker)
            else:
                #If download fails, renavigate tp site in case of ending up
                #somewhere weird
                self.navigateToURL("https://finance.yahoo.com")
                
            
            
                
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

