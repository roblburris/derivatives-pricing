import numpy as np
from binomial_node import BinomialNode

def binomial_pricing(spot, strike, dividend_yield, volatility, time_mature, desired_length, interest_rate):
    """
    Generates a binomial price tree for an American-Style call option
        :param spot: current price of stock in question
        :param strike: given strike/exercise price for options contract
        :param dividend_yield: how much given stock pays out in dividends as a percent
        :param volatility: standard deviation of stock's returns
        :param time_mature: time until option matures, given in days
        :param desired_length: desired number of levels for price tree
        :param interest_rate: annualized risk free interest rate
        :return: calculated value of the option as a float
    """
    len_step = time_mature / desired_length

    increase_factor = np.e ** (volatility * np.sqrt(len_step / 365.0))
    decrease_factor = 1.0 / increase_factor
    exercise_value = strike - spot

    def option_probability():
        """
        Function used to calculate the probability of an up/down move. Meant to simulate geometric
        Brownian motion
        """
        numerator = np.e ** ((interest_rate - dividend_yield) * len_step) - decrease_factor
        denominator = increase_factor - decrease_factor
        return numerator / denominator

    opt_prob = option_probability()

    def generate_tree(node, spot, time):
        """
        Generates binomial price tree two levels at a time
        On the final level, assigns a value to each node
        :param node: reference to BinomialNode
        :param spot: current price at the level
        :param time: current level the tree is on (time period of level is decided earlier)  
        """
        node.left_node = BinomialNode(spot * decrease_factor)
        node.right_node = BinomialNode(spot * increase_factor)
        time += 1

        if time + 1 == desired_length:
            node.left_node.left_node = BinomialNode(spot * decrease_factor * decrease_factor)
            node.left_node.left_node.value = np.max([node.left_node.left_node.root - strike, 0])
            node.left_node.right_node = BinomialNode(spot * decrease_factor * increase_factor)
            node.left_node.right_node.value = np.max([node.left_node.right_node.root - strike, 0])
            node.right_node.left_node = node.left_node.right_node
            node.right_node.right_node = BinomialNode(spot * increase_factor * increase_factor)
            node.right_node.right_node.value = np.max([node.right_node.right_node.root - strike, 0])
        else:
            node.left_node.left_node = generate_tree(
                BinomialNode(spot * decrease_factor * decrease_factor),
                spot * decrease_factor * decrease_factor, time + 1)
            node.left_node.right_node = generate_tree(
                BinomialNode(spot * decrease_factor * increase_factor),
                spot * decrease_factor * increase_factor, time + 1)
            node.right_node.left_node = node.left_node.right_node
            node.right_node.right_node = generate_tree(
                BinomialNode(spot * increase_factor * increase_factor),
                spot * increase_factor * increase_factor, time + 1)

        return node

    def value_node(node):
        """
        Given a binary node, sets the value of that node based on future nodes (must start one level
        behind final level)
        :param node: node being valued
        """
        if node.left_node.value is None:
            node.left_node = value_node(node.left_node)

        if node.right_node.value is None:
            node.right_node = value_node(node.right_node)


        binomial_value = (np.e ** (-interest_rate * len_step)) * (
                opt_prob * node.right_node.value + (1 - opt_prob) * node.left_node.value)
        node.value = np.max([binomial_value, exercise_value])

        return node

    def price_tree(node):
        """
        Prices the entire binary tree working backwards before returning the updated price tree
        :param node: top node of entire binomial price tree
        """
        return value_node(node)
    node = generate_tree(BinomialNode(spot), spot, 0)
    node = price_tree(node)
    return node.value



