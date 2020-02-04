'''Main steps to follow:
    1. Determine flights website
    2. Determine HTML to extract
    3. Make an HTTP request to the webpage
    4. Parse the HTTP response
'''

# import modules
from time import sleep, strftime # sleep between requests
from datetime import datetime
from random import randint # randomize sleep times
import pandas as pd # data processing
import numpy as np 
from selenium import webdriver # web scraping and browser interactions (DOM)
from selenium.webdriver.common.keys import Keys # browser interactions using keyboard keys
from selenium.webdriver.common.proxy import Proxy, ProxyType # for the use of proxies
from bs4 import BeautifulSoup # web scraping static after page loads (static)
import requests
from lxml.html import fromstring
import re # regular expressions
# missing: email management modules

### Functions

def search_flights(flight_input): # this function is very long. See how to optimize it.
    ### To be added - flights back to departure (roundtrip)
    '''
    This function will take care of the input values for the website and click search
    Takes in a dictionary with following keys:
    ### finish description ###
    '''


    from_date = flight_input["from_date"].strftime("%b %-d") # format example: "Jun 9"
    to_date = flight_input["to_date"].strftime("%b %-d")

    sleep(2)
    ### example of first input: from field
    from_xpath = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[1]"
    from_input = driver.find_element_by_xpath(from_xpath)
    from_input.click()
    from_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/destination-picker/div[1]/div[2]/div[2]/input"
    from_input_2 = driver.find_element_by_xpath(from_xpath_2)
    from_input_2.clear()
    from_input_2.send_keys(flight_input["from_city"])
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
    to_input_2.send_keys(flight_input["to_city"])
    sleep(1)
    to_input_2.send_keys(Keys.TAB) # skips to from_date

    ### from_date
    from_date_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/div[4]/div[2]/div[1]/date-input/input"
    sleep(1)
    from_date_input_2 = driver.find_element_by_xpath(from_date_xpath_2)
    from_date_input_2.clear()
    sleep(1)
    from_date_input_2.send_keys(from_date)
    sleep(1)
    from_date_input_2.send_keys(Keys.TAB) # skips to to_date

    ### to_date
    sleep(randint(1,4))
    date_to_xpath_2 = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/div[4]/div[2]/div[3]/date-input/input"
    date_to_input_2 = driver.find_element_by_xpath(date_to_xpath_2)
    date_to_input_2.clear()
    sleep(1)
    date_to_input_2.send_keys(to_date)
    sleep(1)

    ### start search
    date_to_input_2.send_keys(Keys.TAB)
    sleep(1)
    element = driver.switch_to.active_element.send_keys(Keys.RETURN) # press return in button Done -switched to this by pressing TAB
    sleep(2)
    # ### sort flights by price
    # sleep(2) # use wait function instead
    # sort_button = driver.find_element_by_css_selector(".gws-flights-results__sort-menu-icon")
    # sort_button.click()
    # sleep(1)
    # sort_by_price_xpath = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[4]/div[7]/div[1]/div[5]/div[1]/div/div/dropdown-menu/div/div[2]/menu-item[2]"
    # driver.find_element_by_xpath(sort_by_price_xpath).click()
    # sleep(4) # sleep a couple of seconds between each input

def scrape_flights():
    '''
    This function will scrape the data from the website and create a DataFrame with the content
    '''
    print("Inside scrape_flights")
    soup = BeautifulSoup(driver.page_source,"html.parser")
    flights_raw = soup.find_all(
        "li", {
            "class": "gws-flights-results__result-item gws-flights__flex-box gws-flights-results__collapsed"
            }
    ) # list of flights
    
    flights_columns = ["from", "to", "departure_date", "arrival_date", "price_roundtrip", "duration", "n_stops"]
    flights_info_clean = list()

    for flight in flights_raw:
        airports = flight.find(
        "div",{"class": "gws-flights-results__airports flt-caption"})
        from_airport = airports.find_all("span")[0].text
        to_airport = airports.find_all("span")[1].text

        times = flight.find("div",{"class":"gws-flights-results__times"}).find_all("span")
        times = str(times)
        pattern_time = r"[0-1]?[0-9]:[0-6][0-9] [AP]M"
        times = re.findall(pattern_time,times)
        departure_date = times[0] # returns departure time for now, will add datetime
        arrival_date = times[-1] # returns arrival time for now, will add datetime
        
        # price_roundtrip = flight.find(
        # "div",{"class": "gws-flights-results__price"}).text
        price_roundtrip = re.findall(r"\$[1-2]?,?[0-9]{1,3}",str(flight))[0]
        price_roundtrip = int( # convert to int
            price_roundtrip[1:] # remove $ sign
            .replace(",","")) # remove

        duration = flight.find(
            "div",{"class": "gws-flights-results__duration"}).text
        duration_hours = int(
            re.findall(r"([0-9]*)h",duration)[0]
        )
        duration_minutes = int(
            re.findall(r"([0-9]*)m",duration)[0]
        )
        duration_numeric = duration_hours + duration_minutes / 60 # we will be able to transform this to timedelta for data processing

        n_stops = flight.find(
            "div",{"class": "gws-flights-results__stops"}).find(
            "span").text
        if "Nonstop" in n_stops:
            n_stops = 0
        else:
            n_stops = int(n_stops[0])

        flights_info_clean.append([from_airport,to_airport,departure_date,
        arrival_date,price_roundtrip,duration_numeric,n_stops])

    return pd.DataFrame(flights_info_clean,columns=flights_columns)



def scrape_proxy(url = "https://free-proxy-list.net/"):
    '''
    Returns a list of free proxies found on website variable
    '''
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]: # look at first 10 proxies
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    print("Set of poxies scraped: {}".format(proxies))
    return proxies

### Input: This will eventually go in a different script, having list-like objects with dates and cities
## Input dates in datetime format for future automation, this will allow us to iterate over different dates

flight_input = {
    "from_date" : datetime(
        year = 2020,
        month = 6,
        day = 9
    ),
    "from_city":"San Diego",
    "to_date":datetime(
        year = 2020,
        month = 6,
        day = 15
    ),
    "to_city":"Barcelona"
}


### Open browser instance and Google Flights - driver is global variable so we can access from different functions -> create class instead?
proxies = scrape_proxy() 
# connect using proxy
connected = False

while connected == False:
    PROXY = proxies.pop()

    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = PROXY
    # prox.socks_proxy = PROXY , fix socks proxy
    prox.ssl_proxy = PROXY
    print("Changing IP to {}".format(PROXY)) # add from original IP
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    prox.add_to_capabilities(capabilities)


    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    driver = webdriver.Firefox(desired_capabilities=capabilities,firefox_profile=firefox_profile)
    print("Driver capabilities loaded")
    try:
        driver.get("https://www.google.com/flights")
        connected = True



### Web interaction
search_flights(flight_input)

### Web scraping
scraped_flights = scrape_flights()
print(scraped_flights)
### Close browser
# Eventually and when we have multiple requests, the functions will be wrapped into a loop to scrape all the dates and cities
driver.close()