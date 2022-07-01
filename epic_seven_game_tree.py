import math


class node:

    def __init__(self, node_type, action):
        self.node_type = node_type
        self.action = action
        self.children = []
        self.is_terminal = False
        self.value = 0
        