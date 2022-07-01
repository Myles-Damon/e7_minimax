import math

class game:

    def __init__(self, game_stage = 'draft', team_1 = None, team_2 = None, 
                start_of_combat_effects = None, victor = None):
        
        self.game_stage = game_stage
        if team_1 == None:
            self.team_1 = []
        else:
            self.team_1 = team_1
        if team_2 == None:
            self.team_2 = []
        else:
            self.team_2 = team_2

        if start_of_combat_effects == None:
            self.start_of_combat_effects = []
        else:
            self.start_of_combat_effects = start_of_combat_effects

        self.victor = victor

    def draft_character(self, char, team):
        if team == 1:
            x = char.__new__(char)
            x.__init__()
            self.team_1.append(x)
            #char.__new__(char)
        else:
            x = char.__new__(char)
            x.__init__()
            self.team_2.append(x)