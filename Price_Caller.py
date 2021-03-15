""" This file will be used to call the data of the top mentioned tickers from r/WallStreetBets, to start with I'm going to make sure I can call the price properly and display it nicely, then I'll move on to trying to bring in more data."""

import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials

import Data_Read_Write

import csv

List_Of_Stocks = []

Data_Read_Write.Reader("stock.csv", List_Of_Stocks, 'Stock')

Some_Stocks = yf.Tickers(List_Of_Stocks)

print(Some_Stocks)