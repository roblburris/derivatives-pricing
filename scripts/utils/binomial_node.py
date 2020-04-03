class BinomialNode():
    def __init__(self, root, left_node = None, right_node = None):
        self.root = root
        if left_node is not None and right_node is not None:
            self.left_node = left_node
            self.right_node = right_node
        else:
            self.left_node = None
            self.right_node = None