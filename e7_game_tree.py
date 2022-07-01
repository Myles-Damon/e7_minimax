import math
import e7_game
import pickle


class node:

    def __init__(self, node_type, action, game_stage = "blank", chance = 1, team_1 = [], team_2 = []):
        self.node_type = node_type
        self.action = action
        self.chance = chance
        self.children = []
        self.is_terminal = False
        self.value = 0
        self.game = e7_game.game(game_stage, team_1, team_2)

    def spawn_child(self, node_type, action, game_stage, chance = 1, team_1 = None, team_2 = None):
        self.children.append(node(node_type, action, game_stage, chance, team_1, team_2))
        return self.children[len(self.children) - 1]

    def set_value(self, value):
        self.value = value


class tree:

    def __init__(self):
        self.root_node = node(node_type = 'root', action = 'none', game_stage = 'draft')
