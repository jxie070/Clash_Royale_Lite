import math, copy
class Tower:
    towerLibrary={}
    def __init__(self, health, damage, hitrange, hitspeed, image):
        self.health=health
        self.damage=damage
        self.hitrange=hitrange
        self.hitspeed=hitspeed
        self.image=None

    def __repr__(self):
        return f'Tower(health={self.health}, damage={self.damage}, hitrange={self.hitrange}, hitspeed={self.hitspeed})'
    
    def clone(self):
        return copy.deepcopy(self)

    @classmethod
    def createTowerLibrary(cls):
        cls.towerLibrary={
            'PrincessLeft': Princess(3052, 109, 7.5, 0.8, None),
            'PrincessRight': Princess(3052, 109, 7.5, 0.8, None),
            'King': King(4824, 109, 7, 1, None)
        }

class Princess(Tower):
    def __init__(self, health, damage, hitrange, hitspeed, image):
        super().__init__(health, damage, hitrange, hitspeed, image)

    def __repr__(self):
        return f'Princess(health={self.health}, damage={self.damage}, hitrange={self.hitrange}, hitspeed={self.hitspeed})'

class King(Tower):
    def __init__(self, health, damage, hitrange, hitspeed, image):
        super().__init__(health, damage, hitrange, hitspeed, image)

    def __repr__(self):
        return f'King(health={self.health}, damage={self.damage}, hitrange={self.hitrange}, hitspeed={self.hitspeed})'
