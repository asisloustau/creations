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
from bs4 import BeautifulSoup
# missing: email management,

### to-do:create pseudocode for functions

def search_flights():
    '''
    This function will take care of the input values for the website and click search
    '''
    from_city = "LAX"
    to_city = "Madrid"
    date_from = "Jun 9" # we can also use datetime format and convert to this type, this is what Google Flights uses
    date_to = "Jun 21"

    # add: connect using proxy 
 
    sleep(2)
    ### example of first input: from field
    from_xpath = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[1]"
    from_input = driver.find_element_by_xpath(from_xpath)
    from_input.click()
    from_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/destination-picker/div[1]/div[2]/div[2]/input"
    from_input_2 = driver.find_element_by_xpath(from_xpath_2)
    from_input_2.clear()
    from_input_2.send_keys(from_city)
    sleep(1)
    from_input_2.send_keys(Keys.RETURN)
    sleep(1)

    ### to_input
    to_xpath = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[2]"
    to_input = driver.find_element_by_xpath(to_xpath)
    to_input.click()
    to_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/destination-picker/div[1]/div[2]/div[2]/input"
    to_input_2 = driver.find_element_by_xpath(to_xpath_2)
    to_input_2.clear()
    sleep(1)
    to_input_2.send_keys(to_city)
    sleep(1)
    to_input_2.send_keys(Keys.TAB) # skips to date_from

    ### date_from

    date_from_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/div[4]/div[2]/div[1]/date-input/input"
    sleep(1)
    date_from_input_2 = driver.find_element_by_xpath(date_from_xpath_2)
    date_from_input_2.clear()
    sleep(1)
    date_from_input_2.send_keys(date_from)
    sleep(1)
    date_from_input_2.send_keys(Keys.TAB) # skips to date_to

    ### date_to

    sleep(randint(1,4))
    date_to_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/div[4]/div[2]/div[3]/date-input/input"
    date_to_input_2 = driver.find_element_by_xpath(date_to_xpath_2)
    date_to_input_2.clear()
    sleep(1)
    date_to_input_2.send_keys(date_to)
    sleep(1)

    ### start search
    date_to_input_2.send_keys(Keys.TAB)
    sleep(1)
    element = driver.switch_to.active_element.send_keys(Keys.RETURN) # press return in button Done -switched to this by pressing TAB

    ### sort flights by price
    sleep(2) # use wait function instead
    sort_button = driver.find_element_by_css_selector(".gws-flights-results__sort-menu-icon")
    sort_button.click()
    sleep(1)
    sort_by_price_xpath = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[4]/div[7]/div[1]/div[5]/div[1]/div/div/dropdown-menu/div/div[2]/menu-item[2]"
    driver.find_element_by_xpath(sort_by_price_xpath).click()
    sleep(10) # sleep a couple of seconds between each input
    

def scrape_flights():
    '''
    This functin will scrape the data from the website and create a DataFrame with the content
    '''
    # TO-DO: sort by cheapest -dropdown: use XPATH /html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[4]/div[7]/div[1]/div[5]/div[1]/div/div/dropdown-menu/div/div[1]/span[1]
    print("Inside scrape_flights")
    soup = BeautifulSoup(driver.page_source,"html.parser")
    flights = soup.findall("li")
    print("Number of flights scraped: " + len(flights))
    for i in flights:
        print(i)
    



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

# proxies = scrape_proxy() eventually we will save this proxies before calling search_flights and use them
### Open browser instance and Google Flights - driver is global variable so we can access from different functions -> create class instead?
driver = webdriver.Firefox()
driver.get("https://www.google.com/flights")

### Web interaction
search_flights()

### Web scraping
scrape_flights()

### Close browser
driver.close()

