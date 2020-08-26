# -*- coding: utf-8 -*-
"""
Code for import and visualizing stock information from yahoo finance

Created on Wed Aug 26 14:11:42 2020

@author: Tyler
"""

#importing necessary modules
import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


#establishing start and end dates for analysis
start_date = '2010-01-01'
end_date = str(datetime.now().strftime('%Y-%m-%d'))


#tickers for stocks in my portfolio or watchlist 
#AMD
AMD = 'AMD'
#Alibaba
BABA = 'BABA'
#Apple
AAPL = 'AAPL'
#Microsoft
MSFT = 'MSFT'
#Tesla
TSLA = 'TSLA'
#Costco
COST = 'COST'
#Amazon
AMZN = 'AMZN'
#Overstock.com
OSTK = 'OSTK'
#Disney
DIS = 'DIS'
#Boeing
BA = 'BA'
#Moderna
MRNA = 'MRNA'
#Cisco 
CSCO = 'CSCO'
#Facebook
FB = 'FB'

my_portfolio = [AMD, BABA, AAPL, MSFT, TSLA, COST, AMZN]

#function for getting stats of interest of stock for analysis
def get_stats(stock_data):
    return {
            'short_mean': np.mean(stock_data.tail(30)),
            'long_mean': np.mean(stock_data.tail(100)),
            'short_rolling': stock_data.rolling(window=30).mean(),
            'long_rolling': stock_data.rolling(window=100).mean()
            }
    
#function for plotting of stock data that will be loaded !! Modify label accordingly  in this function and get_data function if different stat of interest is used
def create_plot(stock_data, ticker):
    stats = get_stats(stock_data)
    plt.subplots(figsize=(12,8))
    plt.plot(stock_data, label=ticker)
    plt.plot(stats['long_rolling'], label='100 Day Moving Average')
    plt.plot(stats['short_rolling'], label='30 Day Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Adj Close Price')
    plt.legend()
    plt.title('Stock Price over Time')
    plt.show()


#function for cleaning data to clean up NaN's that might be in the stock_data
def clean_data(stock_data, col):
    weekdays = pd.date_range(start=start_date, end=end_date)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')

#function for getting stock information, start_date and end_date defined above
def get_data(ticker):
    try:
        stock_data = data.DataReader(ticker,
                                     'yahoo',
                                     start_date,
                                     end_date)
        adj_close = clean_data(stock_data, 'Adj Close')
        create_plot(adj_close, ticker)
    except RemoteDataError:
            print('No data found for {t}'.format(t=ticker))


get_data(AMD)
