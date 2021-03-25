# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

def openGoogle():
    #Open Firefox
    browser = Firefox()
    #Get google home
    browser.get("https://google.co.uk")
    #Deal with terms and conditions popup/iframe
    
    """
    HARD CODED SLEEP SHOULD BE CORRECTED, HACK FOR NOW
    """
    try:
        sleep(1.0)
        #Switches to iframe of pop up
        browser.switch_to.frame(browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/span/div/div/iframe'))
        #Finds I agree button and clicks
        sleep(0.5)
        browser.find_element_by_id("introAgreeButton").click()
        #returns to default content
        sleep(0.5)
        browser.switch_to.default_content()
    except:
        print("Dealing with Googles terms and conditions pop up failed, check if xpath is still correct")
        browser.close()
    #Returns browser so other functionality can use it. 
    return browser


"""
browser = openGoogle()
sleep(1)



sleep(1)

sleep(1)
Searchbar = browser.find_element_by_name("q")
Searchbar.send_keys("Barclays Stock")
Searchbar.send_keys(Keys.RETURN)
#browser.close()
sleep(1)

Time = 0
while( Time < 10):
    for elem in browser.find_elements_by_xpath('.//span[@class = "IsqQVc NprOob XcVN5d wT3VGc"]'):
        print (elem.text)
    sleep(1)
    Time += 1
    
#<span jsname="vWLAgc" class="IsqQVc NprOob XcVN5d wT3VGc">145.50</span>


#<span jsname="vWLAgc" class="IsqQVc NprOob XcVN5d">804.82</span>

#<span jsname="vWLAgc" class="IsqQVc NprOob XcVN5d fw-price-nc">804.82</span>
"""