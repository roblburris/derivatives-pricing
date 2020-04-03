import yfinance as yf
import yaml
import os
from utils.black_scholes import BlackScholes

bl = BlackScholes(153.18, 200, 0.0014, 0.3019, 0.96)
def get_options(ticker):
    cur_stock = yf.Ticker(ticker)
    print(cur_stock.info)

with open(os.getcwd() + '/params/stocks.yml', 'r') as y:
    print(bl.black_scholes())

