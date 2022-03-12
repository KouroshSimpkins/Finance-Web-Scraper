"""this code will scrape the subreddit 'WallStreetBets' and will
return a text file containing the most mentioned tickers on the subreddit."""

import csv

from datetime import date,timedelta
from dateutil.parser import parse

import requests
from selenium.webdriver import Safari

# Setting up date stuff
today =  date.today()
yesterday = today - timedelta(days=1)
day_index = today.weekday()

with Safari() as driver:

    Weekday_URL = "https://www.reddit.com/r/wallstreetbets/search/?q=%22Daily%20Discussion%20Thread%22%20flair%3A%22Daily%20Discussion%22&restrict_sr=1&sort=new"
    Weekend_URL = "https://www.reddit.com/r/wallstreetbets/search/?q=%22Weekend%20Discussion%22%20flair%3A%22Weekend%20Discussion%22&restrict_sr=1&sort=new"

    if day_index in {1,2,3,4,5}:
        driver.get(Weekday_URL)
    elif day_index in {0,6}:
        driver.get(Weekend_URL)

    links = driver.find_elements_by_xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]')

    for a in links:
        if a.text.startswith('Daily Discussion'):
            date = "".join(a.text.split(' ')[-3:])
            parsed = parse(date)
            if parse(str(yesterday)) == parsed:
                link = a.find_element_by_xpath('../..').get_attribute('href')

        elif a.text.startswith('Weekend'):
            weekend_date = a.text.split(' ')
            parsed_date = weekend_date[-3] + ' ' + weekend_date[-2] + weekend_date[-1] # This parsed date should be the Friday at the start of the weekend
            parsed = parse(parsed_date)

            if day_index == 6: # If the code is running on a Sunday
                friday = today - timedelta(days=2)

            elif day_index == 0: # If the code is running on a Monday
                friday = today - timedelta(days=3)

            if parse(str(friday)) == parsed:
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
comment_list = ",".join(orig_list[0:500]) # Creates a list with which we can query PushShift


def get_comments(comment_list):
    # make an api request to pushshift so that we can read the data in the comments.
    # Pushshift limits the number of comments that can be pulled, so we limit it to asking for 500 comments at a time.
    html = requests.get(f'https://api.pushshift.io/reddit/comment/search?ids={comment_list}&fields=body&size=500')
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
remove = slice(0,500)
cleaned = np.delete(orig_list, remove)
i = 0
while i < len(cleaned):
    print(len(cleaned))
    cleaned = np.delete(cleaned, remove)
    new_comment_list = ",".join(cleaned[0:500])
    newcomments = get_comments(new_comment_list)
    get_stock_list(newcomments, stocks_list)

stock = dict(stock_dict)

Comment_Data = "Comments_Out/Comments"+str(today)+".txt"
with open(Comment_Data, 'w') as w:
    w.write(str(comments))

data = list(zip((stock.keys()), (stock.values())))
Stocks_Data = "Mentions_Out/WSB_Mentions"+str(today)+".csv"
with open(Stocks_Data, 'w') as w:
    writer = csv.writer(w, lineterminator='\n')
    writer.writerow(['Stock','Number of Mentions'])
    for a in data:
        writer.writerow(a)