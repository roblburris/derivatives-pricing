import numpy as np
import scipy.integrate as integrate


def black_scholes(spot, strike, interest_rate, volatility, time_mature):
    """
    Uses Black-Scholes pricing model to determine the value of an option
    :param spot: current price of stock in question
    :param strike: given strike/exercise price for options contract
    :param interest_rate: annualized risk free interest rate
    :param volatility: standard deviation of stock's returns
    :param time_mature: time until option matures, given in days
    :return: float representing value of option according to Black-Scholes 
    """
    def d1(spot, strike, interest_rate, volatility, sqrt_term, time_mature):
        temp1 = 1 / sqrt_term
        temp2 = np.log(spot / strike)
        temp3 = interest_rate + (volatility ** 2) / 2
        temp3 = temp3 * time_mature
        return temp1 * (temp2 + temp3)

    def f(x):
        return np.e ** (-(x ** 2) / 2)

    def prob_function(input):
        return np.divide(1.0, np.sqrt(2 * np.pi)) * integrate.quad(f, np.NINF, input)[0]

    time_mature = time_mature / 365.0
    sqrt_term = volatility * np.sqrt(time_mature)
    term1 = d1(spot, strike, interest_rate, volatility, sqrt_term, time_mature)
    term2 = term1 - sqrt_term
    return prob_function(term1) * spot - (strike * np.e ** (-interest_rate * time_mature)) * prob_function(term2)

