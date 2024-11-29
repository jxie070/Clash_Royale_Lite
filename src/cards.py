import copy
class Card:
    cardLibrary={}
    def __init__(self, name, cost, image, sprite):
        self.name=name
        self.cost=cost
        self.image=image
        self.sprite=sprite

    def __repr__(self):
        return f'Card(name={self.name}, cost={self.cost})'
    
    def clone(self):
        return copy.deepcopy(self)
    
    @classmethod
    def createCardLibrary(cls):
        cls.cardLibrary={
            'Fireball': Spell('Fireball', 4, 'assets/fireball.png', None, 689, 207, 2.5),
            'Arrows': Spell('Arrows', 3, 'assets/arrows.png', None, 366, 93, 4,),
            'Giant': Troop('Giant', 5, 'assets/giant.png', 'assets/giant_sprite.png', 4091, 254, 1.5, 1, 'buildings', 'slow'),
            'Knight': Troop('Knight', 3, 'assets/knight.png', 'assets/knight_sprite.png', 1766, 202, 1, 2, 'ground', 'medium'),
            'Mini-Pekka':Troop('Mini-Pekka', 4, 'assets/mini-pekka.png', 'assets/mini-pekka_sprite.png', 1361, 720, 1, 1, 'ground', 'fast'),
            'Musketeer': Troop('Musketeer', 4, 'assets/musketeer.png', 'assets/musketeer_sprite.png', 720, 218, 1, 6, 'air/ground', 'medium'),
            'Archers': Troop('Archers', 3, 'assets/archers.png', 'assets/archers_sprite.png', 304, 107, 0.9, 6, 'air/ground', 'medium'),
            'Cannon': Building('Cannon', 3, 'assets/cannon.png', 'assets/cannon_sprite.png', 824, 212, 0.9, 5.5, 'ground', 30)
        }


class Troop(Card):
    def __init__(self, name, cost, image, sprite, health, damage, hitspeed, hitrange, targets, speed):
        super().__init__(name, cost, image, sprite)
        self.health=health
        self.damage=damage
        self.hitspeed=hitspeed
        self.hitrange=hitrange
        self.targets=targets
        self.speed=speed

    def __repr__(self):
        return f'Troop(name={self.name}, cost={self.cost}, health={self.health}, damage={self.damage}, hitspeed={self.hitspeed}, hitrange={self.hitrange}, targets={self.targets}, speed={self.speed})'

class Spell(Card):
    def __init__(self, name, cost, image, sprite, damage, towerDamage, radius):
        super().__init__(name, cost, image, sprite)
        self.damage=damage
        self.towerDamage=towerDamage
        self.radius=radius

    def __repr__(self):
        return f'Spell(name={self.name}, cost={self.cost}, damage={self.damage}, towerDamage={self.towerDamage}, radius={self.radius})'
    
class Building(Card):
    def __init__(self, name, cost, image, sprite, health, damage, hitspeed, hitrange, targets, lifespan):
        super().__init__(name, cost, image, sprite)
        self.health=health
        self.damage=damage
        self.hitspeed=hitspeed
        self.hitrange=hitrange
        self.targets=targets
        self.lifespan=lifespan

    def __repr__(self):
        return f'Building(name={self.name}, cost={self.cost}, health={self.health}, damage={self.damage}, hitspeed={self.hitspeed}, hitrange={self.hitrange}, targets={self.targets}, lifespan={self.lifespan})'
    
