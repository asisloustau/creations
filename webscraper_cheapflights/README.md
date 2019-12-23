# Web Scraper - Looking for Error Fares

Caution: This script is not usable yet - Development stage pre-pre-alpha ;)

## Key ideas
- Scrape flight itineraries and prices from different websites and send alerts to email address if the prices are unexpectedly lower than average. 

## Python modules used
- Selenium: Browser interaction - Web requests: We need the DOM content loaded before we scrape data
- BeautifulSoup - Data scraping: Once the website is loaded, it becomes trivial how to scrape the data.
- Re - Regex library: Sometimes it is easy to use regular expresions than BeautifulSoup
- Pandas - Data processing: Extra data cleaning needed after scraping
- Random, sleep - Send requests in time intervals: With this, we will be able to request data every hour/day.
- TBD - gather data and send to email address.

 
