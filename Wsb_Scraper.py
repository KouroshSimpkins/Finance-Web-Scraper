"""this code will scrape the subreddit 'WallStreetBets' and will
return a text file containing the most mentioned tickers on the subreddit."""

from datetime import date,timedelta
from dateutil.parser import parse

import requests
from selenium.webdriver import Safari

yesterday = date.today() - timedelta(days=1)


with Safari() as driver:

    URL = "https://www.reddit.com/r/wallstreetbets/search/?q=%22Daily%20Discussion%20Thread%22%20flair%3A%22Daily%20Discussion%22&restrict_sr=1&sort=new"

    driver.get(URL)