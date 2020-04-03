import numpy as np
import scipy.integrate as integrate


class BlackScholes():
    def __init__(self, spot, strike, interest_rate, volatility, time_mature):
        self.spot = spot
        self.strike = strike
        self.interest_rate = interest_rate
        self.volatility = volatility
        self.time_mature = time_mature
        self.sqrt_term = volatility * np.sqrt(time_mature)


    def d1(self, spot, strike, interest_rate, volatility, sqrt_term, time_mature):
        temp1 = 1 / self.sqrt_term
        temp2 = np.log(spot / strike)
        temp3 = interest_rate + (volatility ** 2) / 2
        temp3 = temp3 * time_mature
        return temp1 * (temp2 + temp3)

    def f(self, x):
        return np.e ** (-(x ** 2) / 2)

    def prob_function(self, input):
        return np.divide(1.0, np.sqrt(2 * np.pi)) * integrate.quad(self.f, np.NINF, input)[0]

    def black_scholes(self):
        term1 = self.d1(self.spot, self.strike, self.interest_rate,
                   self.volatility, self.sqrt_term, self.time_mature)
        term2 = term1 - self.sqrt_term


        return self.prob_function(term1) * self.spot - (self.strike * np.e ** (-self.interest_rate * self.time_mature)) * self.prob_function(term2)

