import yaml
import os
from utils.black_scholes import black_scholes

bl = black_scholes(153.18, 200, 0.0014, 0.3019, 0.96)

print(bl)

# TODO: get API data based on YAML tickers and feed it into black-scholes and binomial pricing models
# TODO: print black-scholes and binomial pricing determined values and whether or not the calls for the stocks are under/overvalued  

