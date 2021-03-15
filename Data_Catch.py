""" This piece of code is only here to copy the data from the CSV_Data, to create the file Stocks_List. I should be able to iterate through every line in each CSV file and copy the text from the first column into Stocks_List.txt. The CSV_Data files each come from the NASDAQ website's stock screener https://www.nasdaq.com/market-activity/stocks/screener?exchange=NASDAQ&render=download, and is up to date according to the name of the file"""

import Data_Read_Write

csv_file = input("Input CSV File: ")
txt_file = input("Output TXT File: ")

Symbols = []

Data_Read_Write.Reader(csv_file, Symbols, 'Symbol')

Data_Read_Write.Writer(txt_file, Symbols)

""" This code works using the built in function, however it would also be possible to read the data from the CSV file using pandas. This is just my own implementation to prove that I can do it and to help me learn how, I will probably switch to pandas when I come back to this."""