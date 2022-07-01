import math

passive_types = ["start of combat", "end of turn", "on kill", "on non-attack", "on attack",
                "on aoe"]

class Character:
    def __init__(self, name = 'a', attack = 2, defense = 1, hp = 10, speed = 1, crit_chance = 0.15, crit_damage = 1.50, effectiveness = 0.0, effect_resistance = 0.0, dual_attack_chance = 5.0, artifact = None):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.HP = hp
        self.speed = speed
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.effectiveness = effectiveness
        self.effect_resistance = effect_resistance
        self.dual_attack_chance = dual_attack_chance
        self.combat_readiness = 0.0
        self.status_effects = []
        self.buffs = []
        self.passives = []
        self.ability_cooldowns = [0, 0, 0]
        self.artifact = None

    # WILL BE OVERLOADED PER-UNIT, JUST HERE FOR PREDICTABILITY'S SAKE
    def skill_one(self, target):
        pass

    def push_cr(self, cr_push):
        self.combat_readiness += cr_push



class Straze(Character):

    def __init__(self):
        super().__init__("Straze", attack = 10, speed = 4, crit_chance=1, crit_damage=3)

    def skill_one(self, target):
        cr_push_amount = 0.15
        skill_damage = self.attack * 1 - target.defense
        return [[target.name, 'damage', skill_damage], 
        [self.name, 'cr push', cr_push_amount]]

class Pavel(Character):

    def __init__(self):
        super().__init__("Pavel", attack = 7, speed = 10, crit_chance=1, crit_damage=3)

    def skill_one(self, target):
        skill_damage = self.attack * 1 - target.defense
        return [[target.name, 'damage', skill_damage]]

class Emilia(Character):

    def __init__(self):
        super().__init__("Emilia", defense = 3, speed = 7, crit_chance=0.15, crit_damage=1.5)

    def skill_one(self, target):
        skill_damage = self.attack * 1 - target.defense
        heal_amount = self.HP * 0.4
        return [[target.name, 'damage', skill_damage], 
        [self.name, 'heal', heal_amount]]

    def skill_two(self, target):
        cr_push_amount = 0.4
        return [[target.name, 'cr push', cr_push_amount]]


class Crozet(Character):

    def __init__(self):
        super().__init__("Crozet", defense = 4, speed = 3, crit_chance=0.15, crit_damage=1.5)

    def skill_one(self, target):
        skill_damage = self.attack * 1 - target.defense
        debuff_chance = self.effectiveness - target.effect_resistance
        debuff_duration = 1
        if debuff_chance < 0:
            debuff_chance = 0
        elif debuff_chance > 100:
            debuff_chance = 85
        return [[target.name, 'damage', skill_damage], 
        [target.name, 'on_attack_debuff', 'attack_down', debuff_chance, debuff_duration]]

class Hwayoung(Character):

    def __init__(self):
        super().__init__()
        shield_amount = 0.45 * self.attack
        self.passives.append([self.name, 'start of combat', 'barrier', shield_amount])
        self.passives.append([self.name, 'end of turn', 'barrier', shield_amount])

    def skill_one(self, target):
        #IGNORES 70% OF TARGET'S DEFENSE
        skill_damage = self.attack * 1 - 0.3 * target.defense
        return [[target.name, 'damage', skill_damage]]

class Luna(Character):

    def __init__(self):
        super().__init__("Luna", attack = 7, speed = 6, crit_chance=1, crit_damage=3)

    def skill_one(self, target):
        cr_push_amount = 0.15
        skill_damage = self.attack * 1 - target.defense
        return [[target.name, 'damage', skill_damage], [self.name, 'cr_push', cr_push_amount]]

class Krau(Character):

    def __init__(self):
        super().__init__("Krau", defense = 4, speed = 3, crit_chance=0.15, crit_damage=1.5)

    def skill_one(self, target):
        skill_damage = self.attack * 1 - target.defense
        debuff_chance = self.effectiveness - target.effect_resistance
        debuff_duration = 1
        if debuff_chance < 0:
            debuff_chance = 0
        elif debuff_chance > 100:
            debuff_chance = 75
        return [[target.name, 'damage', skill_damage], 
        [target.name, 'on_attack_debuff', 'provoke', debuff_chance, debuff_duration]]

class Zahhak(Character):

    def __init__(self):
        super().__init__("Zahhak", attack = 7, speed = 6, crit_chance=1, crit_damage=3)

    def skill_one(self, target):
        skill_damage = self.attack * 1 - target.defense
        return [[target.name, 'damage', skill_damage]]

class Celine(Character):

    def __init__(self):
        super().__init__("Celine", attack = 7, speed = 6, crit_chance=1, crit_damage=3)

    def skill_one(self, target):
        skill_damage = self.attack * 1 - target.defense
        return [[target.name, 'damage', skill_damage]]

class Landy(Character):

    def __init__(self):
        super().__init__(name="Landy", attack = 7, speed = 5, crit_chance=1, crit_damage=3)

    def skill_one(self, target):
        cr_push_amount = 0.15
        skill_damage = self.attack * 1 - target.defense
        return [[target.name, 'damage', skill_damage], [self.name, 'cr_push', cr_push_amount]]

character_list = [Landy, Celine, Zahhak, Krau, Luna, Hwayoung, Crozet, Emilia, Pavel, Straze]  