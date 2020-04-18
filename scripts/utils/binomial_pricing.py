import numpy as np
from binomial_node import BinomialNode

def binomial_pricing(spot, strike, dividend_yield, volatility, desired_length, len_step):
    """
    Generates a binomial price tree
    """
    
    increase_factor = np.e ** (volatility * np.sqrt(len_step))
    decrease_factor = 1.0 / increase_factor

    def generate_tree(node, spot, time):
        """
        Generates binomial price tree two levels at a time using recursion
        :param node: reference to BinomialNode
        :param spot: current price at the level
        :param time: current level the tree is on (time period of level is decided earlier)  
        """
        node.left_node = BinomialNode(spot * decrease_factor)
        node.right_node = BinomialNode(spot * increase_factor)
        
        if time + 1 == desired_length:
            node.left_node.left_node = BinomialNode(spot * decrease_factor * decrease_factor)
            node.left_node.right_node = BinomialNode(spot * decrease_factor * increase_factor)
            node.right_node.left_node = node.left_node.right_node
            node.right_node.right_node = BinomialNode(spot * increase_factor * increase_factor)
        else:
            node.left_node.left_node = generate_tree(BinomialNode(spot * decrease_factor * decrease_factor), spot * decrease_factor * decrease_factor, time + 2)
            node.left_node.right_node = generate_tree(BinomialNode(spot * decrease_factor * increase_factor), spot * decrease_factor * increase_factor, time + 2)
            node.right_node.left_node = node.left_node.right_node
            node.right_node.right_node = generate_tree(BinomialNode(spot * increase_factor * increase_factor), spot * increase_factor * increase_factor, time + 2)
            
        return node
    
