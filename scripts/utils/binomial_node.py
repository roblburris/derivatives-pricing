class BinomialNode():
    """
    Definition of BinomialNode, used in a binomial pricing tree
    """
    def __init__(self, data, left_node = None, right_node = None):
        """
        Creates a BinomialNode
        :param data: float stored in this BinomialNode
        :param left_node: reference to another BinomialNode, set to null if not specified
        :param right_node: reference to another BinomialNode, set to null if not specified
        """
        self.root = data
        if left_node is not None and right_node is not None:
            self.left_node = left_node
            self.right_node = right_node
        else:
            self.left_node = None
            self.right_node = None