"""this code will scrape the subreddit 'WallStreetBets' and will return a text file containing the most mentioned tickers on the subreddit."""

from datetime import date,timedelta
from dateutil.parser import parse

import requests
from selenium.webdriver import Safari

import csv

yesterday = date.today() - timedelta(days=2) # Just a workaround so I can get this code to run on a Sunday

with Safari() as driver:

    URL = "https://www.reddit.com/r/wallstreetbets/search/?q=%22Daily%20Discussion%20Thread%22%20flair%3A%22Daily%20Discussion%22&restrict_sr=1&sort=new"

    driver.get(URL)

    links = driver.find_elements_by_xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]')

    for a in links:
        if a.text.startswith('Daily Discussion Thread'):
            date = "".join(a.text.split(' ')[-3:])
            parsed = parse(date)
            if parse(str(yesterday)) == parsed:
                link = a.find_element_by_xpath('../..').get_attribute('href')

    stock_link = link.split('/')[-3]

    html = requests.get(f'https://api.pushshift.io/reddit/submission/comment_ids/{stock_link}')

    raw_comment_list = html.json()


with open('Stocks_List.txt', 'r') as document:
    stocks = document.readlines() # Read every line of the Stocks_List document
    stocks_list = [] # Initialise a list called stocks_list (will store the tickers from the txt file)
    for a in stocks:
        a = a.replace('\n',' ')
        stocks_list.append(' '+a) # Add the ticker to the end of the stocks_list


import numpy as np

orig_list = np.array(raw_comment_list['data']) # Creates a numpy array from the raw comment list we collected above
comment_list = ",".join(orig_list[0:1000]) # Creates a list with which we can query PushShift


def get_comments(comment_list):

    html = requests.get(f'https://api.pushshift.io/reddit/comment/search?ids={comment_list}&fields=body&size=1000')
    newcomments = html.json()
    return newcomments

comments = dict()

from collections import Counter
stock_dict = Counter()
def get_stock_list(newcomments,stocks_list):
    for a in newcomments['data']:
        for ticker in stocks_list:
            if ticker in a['body']:
                stock_dict[ticker] += 1
                comments[a['body']] = ticker

orig_list = np.array(raw_comment_list['data'])
remove = slice(0,1000)
cleaned = np.delete(orig_list, remove)
i = 0
while i < len(cleaned):
    print(len(cleaned))
    cleaned = np.delete(cleaned, remove)
    new_comment_list = ",".join(cleaned[0:1000])
    newcomments = get_comments(new_comment_list)
    get_stock_list(newcomments, stocks_list)

stock = dict(stock_dict)

with open('Comments.txt', 'w') as w:
    w.write(str(comments))

data = list(zip((stock.keys()), (stock.values())))
with open('stock.csv', 'w') as w:
    writer = csv.writer(w, lineterminator='\n')
    writer.writerow(['Stock','Number of Mentions'])
    for a in data:
        writer.writerow(a)