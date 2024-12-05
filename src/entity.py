import copy, time, math
class Entity():
    #movement string to tiles/second
    movementDict={
        'slow': 0.75,
        'medium': 1,
        'fast': 1.5,
        'very-fast': 2
    }
    #wrapper class that allows Cards and Tower classes to use the same functions without having to copy/paste
    def move(self, app, friendlyPosition, nextRow, nextCol):
        tilesPerSecond=Entity.movementDict[self.speed]
        currCol, currRow = friendlyPosition
        #dRow and dCol should be the signs
        dRow, dCol = nextRow-math.floor(currRow), nextCol-math.floor(currCol)
        return (currCol + app.dt*tilesPerSecond*dCol, currRow + app.dt*tilesPerSecond*dRow)

    def attackTarget(self, app, enemyUnit, enemyIndex, otherList):
        #No need to pop, processUnits already pops units out
        self.targeting=(enemyUnit, enemyIndex, otherList)
        currTime=time.time()
        if(currTime-self.lastAttackTime>=self.hitspeed):
            enemyUnit.health=max(0, enemyUnit.health-self.damage)
            self.lastAttackTime=currTime
            if(enemyUnit.health<=0):
                self.targeting=None
                if(isinstance(enemyUnit, King)):
                    app.gameOver=True
                #print(otherList, enemyIndex)

    def findTarget(self, selfPosition, otherList):
        closestTarget=None
        closestDistance=None
        closestPosition=None
        closestIndex=None
        for enemyIndex, (enemyUnit, enemyPosition) in enumerate(otherList):
            if not self.sharedTarget(enemyUnit):
                continue
            currDistance = self.getDistance(selfPosition, enemyPosition)
            if(closestTarget==None or currDistance<closestDistance):
                closestTarget=enemyUnit
                closestDistance=currDistance
                closestPosition=enemyPosition
                closestIndex=enemyIndex
        return closestTarget, closestDistance, closestPosition, closestIndex
    
    def sharedTarget(self, other):
        return len(set(self.targets)&set(other.targetted))>=1

    def getDistance(self, selfPosition, otherPosition):
        #friendlyIndex=self.findIndex(app, True)
        friendC, friendR = selfPosition
        #enemyIndex=enemyUnit.findIndex(app, False)
        enemyC, enemyR = otherPosition
        diffC, diffR =(enemyC-friendC), (enemyR-friendR)
        return math.sqrt(diffC**2 + diffR**2)

class Card(Entity):
    cardLibrary={}
    def __init__(self, name, cost, image, sprite):
        self.name=name
        self.cost=cost
        self.image=image
        self.sprite=sprite
        self.lastAttackTime=0
        self.targeting=None

    def __repr__(self):
        return f'Card(name={self.name}, cost={self.cost})'
    
    def clone(self):
        return copy.deepcopy(self)
    
    @classmethod
    def createCardLibrary(cls):
        cls.cardLibrary={
            'Fireball': Spell('Fireball', 4, 'assets/fireball.png', None, 689, 207, 2.5),
            'Arrows': Spell('Arrows', 3, 'assets/arrows.png', None, 366, 93, 4,),
            'Giant': Troop('Giant', 5, 'assets/giant.png', 'assets/giant_sprite.png', 4091, 254, 1.5, 2, ['buildings'], ['ground'], 'slow'),
            'Knight': Troop('Knight', 3, 'assets/knight.png', 'assets/knight_sprite.png', 1766, 202, 1, 2, ['ground'], ['ground'], 'medium'),
            'Mini-Pekka':Troop('Mini-Pekka', 4, 'assets/mini-pekka.png', 'assets/mini-pekka_sprite.png', 1361, 720, 1, 2, ['ground'], ['ground'], 'fast'),
            'Musketeer': Troop('Musketeer', 4, 'assets/musketeer.png', 'assets/musketeer_sprite.png', 720, 218, 1, 6, ['air', 'ground'], ['ground'], 'medium'),
            'Archers': Troop('Archers', 3, 'assets/archers.png', 'assets/archers_sprite.png', 304, 107, 0.9, 6, ['air', 'ground'], ['ground'], 'medium'),
            'Cannon': Building('Cannon', 3, 'assets/cannon.png', 'assets/cannon_sprite.png', 824, 212, 0.9, 5.5, ['ground'], ['ground'], 30, 824)
        }

    

class Troop(Card):
    def __init__(self, name, cost, image, sprite, health, damage, hitspeed, hitrange, targets, targetted, speed):
        super().__init__(name, cost, image, sprite)
        self.health=health
        self.damage=damage
        self.hitspeed=hitspeed
        self.hitrange=hitrange
        self.targets=targets
        self.speed=speed
        self.targetted=targetted

    def __repr__(self):
        return f'Troop(name={self.name})'

class Spell(Card):
    def __init__(self, name, cost, image, sprite, damage, towerDamage, radius):
        super().__init__(name, cost, image, sprite)
        self.damage=damage
        self.towerDamage=towerDamage
        self.radius=radius

    def __repr__(self):
        return f'Spell(name={self.name})'
    
class Building(Card):
    def __init__(self, name, cost, image, sprite, health, damage, hitspeed, hitrange, targets, targetted, lifespan, initialHealth):
        super().__init__(name, cost, image, sprite)
        self.health=health
        self.damage=damage
        self.hitspeed=hitspeed
        self.hitrange=hitrange
        self.targets=targets
        self.targetted=targetted
        self.lifespan=lifespan
        self.initialHealth=initialHealth

    def __repr__(self):
        return f'Building(name={self.name})'
    
class Tower(Entity):
    towerLibrary={}
    def __init__(self, health, damage, hitrange, hitspeed, targets, targetted, image):
        self.health=health
        self.damage=damage
        self.hitrange=hitrange
        self.hitspeed=hitspeed
        self.targets=targets
        self.targetted=targetted
        self.image=None
        self.lastAttackTime=0
        self.targeting=None

    def __repr__(self):
        return f'Tower(health={self.health})'
    
    def clone(self):
        return copy.deepcopy(self)

    @classmethod
    def createTowerLibrary(cls):
        #king:4824, tower:3052
        cls.towerLibrary={
            'PrincessLeft': PrincessLeft(3052, 109, 9.5, 0.8, ['air', 'ground', 'buildings'], ['air', 'ground', 'buildings'], None),
            'PrincessRight': PrincessRight(3052, 109, 9.5, 0.8, ['air', 'ground', 'buildings'], ['air', 'ground', 'buildings'], None),
            'King': King(4824, 109, 8, 1, ['air', 'ground', 'buildings'], ['air', 'ground', 'buildings'], False, None)
        }

class PrincessLeft(Tower):
    def __init__(self, health, damage, hitrange, hitspeed, targets, targetted, image):
        super().__init__(health, damage, hitrange, hitspeed, targets, targetted, image)

    def __repr__(self):
        return f'Princess(health={self.health})'

class PrincessRight(Tower):
    def __init__(self, health, damage, hitrange, hitspeed, targets, targetted, image):
        super().__init__(health, damage, hitrange, hitspeed, targets, targetted, image)

    def __repr__(self):
        return f'Princess(health={self.health})'

class King(Tower):
    def __init__(self, health, damage, hitrange, hitspeed, targets, targetted, active, image):
        super().__init__(health, damage, hitrange, hitspeed, targets, targetted, image)
        self.active=active
    def __repr__(self):
        return f'King(health={self.health})'
