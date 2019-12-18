'''Main steps to follow:
    1. Determine flights website
    2. Determine HTML to extract
    3. Make an HTTP request to the webpage
    4. Parse the HTTP response
'''

# import modules
import re
from time import sleep, strftime # sleep between requests
from random import randint # randomize sleep times
import pandas as pd
import numpy as np 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# missing: email management,

### to-do:create pseudocode for functions

def search_flights():
    '''
    This function will take care of the input values for the website and click search
    '''
    driver = webdriver.Firefox()
    driver.get("https://www.google.com/flights")
    ### example of first input: from field
    # from_input=driver.find_element_by_name(#add input here)
    # from_input.clear()
    # from_input.send_keys("San Diego")
    
    ### to_input

    ### date_from

    ### date_to

    # after filling all the fields, click on search button
    sleep(10) # sleep a couple of seconds between each input
    driver.close()

def scrape_flights():
    '''
    This functin will scrape the data from the website and create a DataFrame with the content
    '''
    pass


# to-do: Proxy implementation
# function 1: scrape list of proxies from https://free-proxy-list.net/
def scrape_proxy(website = "https://free-proxy-list.net/"):
    '''
    Returns a list of free proxies found on defined website
    '''
    driver = webdriver.Firefox()
    driver.get(website)
    xpath='/html/body/section[1]/div/div[2]/div/div[2]/div/table/tbody'
    rows = driver.find_elements_by_xpath(xpath)
    rows_text = [element.text for element in rows]
    proxy_list = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',''.join(rows_text))
    sleep(1)
    driver.close()
    return proxy_list


print(scrape_proxy()) #test function
# function 2: try proxies (Starting with newest) to connect -> this will go in scrape function