import math, pickle, copy
import e7_characters, e7_game_tree

current_character_turn = None
next_character_turn = None

TEST = False

draft_phase_strings = ['blue draft first character', 'red draft first character',
                        'red draft second character', 'blue draft second character',
                        'blue draft third character', 'red draft third character',
                        'red draft fourth character', 'blue draft fourth character',
                        'blue draft fifth character', 'red draft fifth character']
team_draft_shortcut = [1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 0]

def print_all_drafts(node):

    for child in node.children:
        if child.game.game_stage == 'draft':
            print_all_drafts(child)
        elif node.game.game_stage == 'draft':
            print("Draft\n-----------")
            print("\nTeam 1:\t\t\tTeam 2:")
            assert len(node.game.team_1) == len(node.game.team_2)
            team_size = len(node.game.team_1)
            for char_index in range(team_size):
                print(node.game.team_1[char_index].name, "\t\t\t", node.game.team_2[char_index].name)
        else:
            print("node supplied is past the draft stage")




def print_test_draft(tree):
    
    node = tree.root_node
    while(len(node.children) > 0 ):
        if node.children[0].game.game_stage == 'draft':
            node = node.children[0]
        else:
            break

    team_size = len(node.game.team_1)
    print("\nprinting test draft")
    print("\nTeam 1:\t\t\tTeam 2:")
        
    for char_index in range(team_size):
        print(node.game.team_1[char_index].name, "\t\t\t", node.game.team_2[char_index].name)

def draft_phase(tree, team_1, team_2, team_size = 2):

    def draft(draft_node, draft_stage = 0, team_drafting = 1, remaining_char_list = e7_characters.character_list) -> e7_game_tree.node:
        if draft_stage < 10:
            for char in remaining_char_list:
                d = draft_node.spawn_child('action - draft', draft_phase_strings[draft_stage], 'draft',
                    1,
                    copy.deepcopy(draft_node.game.team_1),
                    copy.deepcopy(draft_node.game.team_2))
                #d = draft_node.children[len(draft_node.children) - 1]
                d.game.draft_character(char, team_drafting)
                new_char_list = copy.deepcopy(remaining_char_list)
                new_char_list.remove(char)
                draft_node.children.append(draft(d, draft_stage + 1, team_draft_shortcut[draft_stage + 1], new_char_list))
            return draft_node
        elif draft_stage == 10:
            assert len(draft_node.game.team_1) > 0, "lol"
            assert len(draft_node.game.team_2) > 0, "olo"
            #print("lmao")
            #print(len(draft_node.game.team_1))
            #for char in draft_node.game.team_1:
                #print(char.name)
            return None


    node = tree.root_node

    print("team size: ", team_size)
    if TEST:
        team_1.append(e7_characters.Emilia())
        node_1 = node.spawn_child('action - draft', 'blue draft first character', 'draft', 
        1, 
        team_1,
        team_2)

        team_2.append(e7_characters.Pavel())
        node_2 = node_1.spawn_child('action - draft', 'red draft first character', 'draft', 
        1,
        team_1, 
        team_2)

        team_2.append(e7_characters.Straze())
        node_3 = node_2.spawn_child('action - draft', 'red draft second character', 'draft',
        1,
        team_1,
        team_2)

        team_1.append(e7_characters.Crozet())
        node_4 = node_3.spawn_child('action - draft', 'blue draft second character', 'draft',
        1,
        team_1,
        team_2)

        print_test_draft(tree)
    else:
        char_list = e7_characters.character_list
        node = draft(node, draft_stage=0, team_drafting=1, remaining_char_list=char_list)
    return node

#START OF COMBAT EFFECTS (GUIDING LIGHT, HWAYOUNG SHIELD, FCC SHIELD, ETC.)
def start_of_combat_effects(game):
    for start_of_combat_effect in game.start_of_combat_effects:
        #apply each effect
        pass

def pre_first_attack(game):
    highest_speed = 0
    assert len(game.team_1) > 0, "empty team 1!"
    assert len(game.team_2) > 0, "empty team 2!"
    for character in game.team_1 + game.team_2:
        #print(character.name, "  ", character.speed)
        if character.speed > highest_speed:
            highest_speed = character.speed
   
    assert highest_speed > 0, "highest speed = 0"
    #SET INITIAL CR
    for character in game.team_1 + game.team_2:
        character.push_cr(character.speed / highest_speed)

def print_cr(game):
    cr_dict = {}
    for character in game.team_1 + game.team_2:
        cr_dict.update({character.name: character.combat_readiness})
    for k in sorted(cr_dict, key=cr_dict.get, reverse=True):
        print(k, "\t\t", cr_dict[k])

def debug_print_cr(game):
    print_cr(game)

def combat_turn(game):


    #UNIT WHICH RETURNS LOWEST CALCULATED COEFFICIENT IS NEXT TO TAKE THE TURN
    def calculate_next_turn_coefficient(char_speed, char_cr) -> float:
        return char_speed / (1.0 - char_cr)

    # lol
    def go_next():
        lowest_next_turn_coefficient = 1.0
        for character in game.team_1 + game.team_2:
            global next_character_turn
            x = calculate_next_turn_coefficient(character.speed, character.cr)
            if x < lowest_next_turn_coefficient:
                lowest_next_turn_coefficient = x
                next_character_turn = character
        for character in game.team_1 + game.team_2:
            character.cr = character.cr + character.speed * lowest_next_turn_coefficient
        return None

    # will be finished later


    return None
"""
""" 

def get_value_of_node(node) -> int:
    if node.node_type == 'action - draft':
        if node.game.team_1.count(e7_characters.Pavel) > 0:
            return 1
        else:
            return -1
    elif node.is_terminal:
        if node.game.victor == 1:
            return 1
        elif node.game.victor == 2:
            return -1
        else:
            return len(node.game.team_1) - len(node.game.team_2)
    else:
        return 0

def get_end_of_draft(tree) -> e7_game_tree.node:
    node = tree.root_node
    while(len(node.children) > 0):
        if node.children[0].game.game_stage == 'draft':
            node = node.children[0]
        else:
            break

    return node

def save_tree(tree):
    with open("test.pickle", "wb") as outfile:
        pickle.dump(tree, outfile)
        print("tree written to test.pickle")

def reconstruct_tree() -> e7_game_tree.tree:
    print("\nreconstructing tree from pickle file")
    with open("test.pickle", "rb") as infile:
        reconstructed_tree = pickle.load(infile)
        return reconstructed_tree

def main_combat_loop(node):
    start_of_combat_effects(node.game)
    pre_first_attack(node.game)
    debug_print_cr(node.game)


def main():
    main_tree = e7_game_tree.tree()
    main_tree = draft_phase(main_tree, [], [], 5)
    save_tree(main_tree)

    recon_tree = reconstruct_tree()
    #print_test_draft(recon_tree)

    print_all_drafts(recon_tree.root_node)

    end_of_draft = get_end_of_draft(recon_tree)

    print("The value of this draft is", get_value_of_node(end_of_draft))
    #main_combat_loop(end_of_draft)


    return None



if __name__ == "__main__":
    main()
