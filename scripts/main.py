import yaml, os
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import yfinance as yf
from black_scholes import black_scholes
from binomial_pricing import binomial_pricing

# Get user-specified specs from YAML file
os.chdir("..")
with open(os.path.join(os.getcwd(), 'params/stocks.yml')) as f:
    specs = yaml.safe_load(f)

tickers = specs[0]['stocks']

# Declare Constants from YAML File (i.e. risk free interest rate)
desired_constants = specs[1]['specified_params']
EXP_TIME = desired_constants[0]['time_to_exp']
DESIRED_PERCENT = desired_constants[1]['percent_increase']
INTEREST_RATE = desired_constants[2]['interest']
NUM_LEVELS = desired_constants[3]['desired_levels']
DESIRED_EXP_DATE = timedelta(days=EXP_TIME) + date.today()

final_data = []

def get_options():
    """
    Gets current stock price and current options value for an option with strike price greater than the spot price by the specified percentage. 
    Grabs the option closest aligning to the desired time to expiration. Also grabs dividend yield and volatility for each stock.
    """

    def get_volatility(ticker):
        """
        Computes a stock's volatility based on historical data
        :param ticker: reference to yfinance ticker
        :return: float representing volatility of the stock
        """
        df = ticker.history(period="12mo")
        return df['Close'].apply(lambda x: np.log(1 + x)).std()

    for ticker in tickers:
        complete_info = {}
        print(ticker)
        stock = yf.Ticker(ticker)
        volatility = get_volatility(stock)
        dividend_yield = (stock.info['dividendYield'], 0)[stock.info['dividendYield'] == None]
        spot = (stock.info['previousClose'], stock.info['ask'])[stock.info['ask'] != 0]
        complete_info['spot'] = spot
        desired_strike = spot * (1 + (DESIRED_PERCENT * 0.01))
        closest_date = ""
        min_diff = abs(datetime.strptime(stock.options[0], '%Y-%m-%d').date() - DESIRED_EXP_DATE)
        
        for exp_date in stock.options:
            cur_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
            diff = abs(cur_date - DESIRED_EXP_DATE)
            if (diff < min_diff):
                closest_date = exp_date
                min_diff = diff
        
        time_to_exp = (datetime.strptime(closest_date, '%Y-%m-%d').date()- date.today()).days

        # Get options chain for closest date with puts if desired_percent is negative and calls otherwise
        opt_chain = (stock.option_chain(closest_date).puts, stock.option_chain(closest_date).calls)[DESIRED_PERCENT > 0]
        complete_info['Expiration Date'] =  closest_date
        opt_chain = opt_chain.iloc[(opt_chain['strike']-desired_strike).abs().argsort()[:1]]
        
        complete_info['Strike'] = opt_chain.iloc[0]['strike']
        complete_info['Contract Name'] = opt_chain.iloc[0]['contractSymbol']
        complete_info['Last Price'] = opt_chain.iloc[0]['lastPrice']

        # Call Black-Scholes and Binomial Pricing Models
        complete_info['Black Scholes'] = []
        complete_info['Binomial Tree'] = []
        complete_info['Black Scholes'].append(black_scholes(spot, complete_info['Strike'], INTEREST_RATE, volatility, time_to_exp))
        complete_info['Binomial Tree'].append(binomial_pricing(spot, complete_info['Strike'], dividend_yield, volatility, time_to_exp, NUM_LEVELS, INTEREST_RATE))
        complete_info['Black Scholes'].append(("overvalued", "undervalued")[complete_info['Black Scholes'][0] <  complete_info['Last Price']])
        complete_info['Binomial Tree'].append(("overvalued", "undervalued")[complete_info['Binomial Tree'][0] <  complete_info['Last Price']])

        final_data.append(complete_info)

get_options()

# Write to YAML File
with open('/params/results.yml', 'w') as f:
    yaml.dump(final_data, f)
