from cmu_graphics import *
from game import Game
from cards import Card, Building, Troop, Spell
from tower import Tower, Princess, King
from node import Node, astar
import math, copy, random

#Jack Xie, jackx2
#This project in its entirety, the concepts, the sprites, etc. are taken from Supercell's game Clash Royale.
#This project is meant to mimic some of the core features of Clash Royale
#TODO:
#1. write onStep function to animate cards
#2. draw each card in units with their position
#3. write algorihm that finds each card's target, whether or not target is in range, and add pathing blocks to board

def onAppStart(app):
    app.stepsPerSecond=60
    app.width=480
    app.height=800
    app.gold=0
    app.gems=0
    app.experience=0
    app.username='Atayxii'
    app.deck=['Archers', 'Knight', 'Giant', 'Fireball', 'Arrows', 'Cannon', 'Mini-Pekka', 'Musketeer']
    app.botDeck=['Archers', 'Knight', 'Giant', 'Fireball', 'Arrows', 'Cannon', 'Mini-Pekka', 'Musketeer']
    app.font='supercell_magic.ttf'

def main_redrawAll(app):
    #on main start is on app start
    #background
    drawImage('assets/bg.png', 0, 0)
    #gui
    drawImage('assets/battle_button.png', 115, 400, width=250, height=250)
    drawLabel('Battle', 240, 525, fill='white', size=48, bold=True, border='black', borderWidth=2)
    drawImage('assets/arena1.png', 65, 150, width=350, height=300)
    drawRect(0, 8, 480, 52, fill=rgb(4, 21, 45), opacity=75)
    drawImage('assets/gem_icon.png', 420, 10, width=50, height=50)
    drawLabel(app.gems, 420, 35, size=32, bold=True, fill='white', align='right')
    drawImage('assets/gold_icon.png', 280, 10, width=50, height=50)
    drawLabel(app.gold, 275, 35, size=32, bold=True, fill='white', align='right')
    drawImage('assets/experience_icon.png', 10, 12, width=40, height=40)
    drawLabel(app.experience, 60, 35, size=32, bold=True, fill='white', align='left')
    drawImage('assets/settings_icon.png', 15, 250, width=75, height=75)
    drawLabel(f'Welcome, {app.username}' if app.username!='' else 'Welcome!', 240, 120, size=48, fill='white', bold=True)
    #chest slots
    drawImage('assets/chest_slot.png', 0, 580, width=120, height=150)
    drawImage('assets/chest_slot.png', 120, 580, width=120, height=150)
    drawImage('assets/chest_slot.png', 240, 580, width=120, height=150)
    drawImage('assets/chest_slot.png', 360, 580, width=120, height=150)
    #bottom bar
    drawRect(0, 740, 480, 60, fill=rgb(67, 81, 98))
    drawRect(0, 735, 480, 5, fill=rgb(111, 137, 167))
    #cards icon
    drawImage('assets/card_icon.png', 80, 740, width=55, height=55)
    drawLabel('Cards>', 107.5, 790, fill='white', size=17, bold=True)
    #shop icon
    drawImage('assets/shop_icon.png', 347.5, 740, width=55, height=55)
    drawLabel('<Shop', 375, 790, fill='white', size=17, bold=True)
    #glow to indicate which screen
    drawRect(180, 740, 120, 60, fill=rgb(114, 145, 176), opacity=30)
    #battle icon
    drawImage('assets/battle_icon.png', 212.5, 740, width=55, height=55)
    drawLabel('<Battle>', 240, 790, fill='white', size=17, bold=True)   

#when on main screen, pressing left should go to cards; pressing right should go to shop
def main_onKeyPress(app, key):
    if(key=='left'):
        setActiveScreen('cards')
    elif(key=='right'):
        setActiveScreen('shop')

def main_onMousePress(app, mouseX, mouseY):
    selected=main_findButton(app, mouseX, mouseY)
    if(selected!=None):
        if(selected=='cardButton'):
            setActiveScreen('cards')
        elif(selected=='shopButton'):
            setActiveScreen('shop')
        elif(selected=='settingsButton'):
            setActiveScreen('settings')
        elif(selected=='battleButton'):
            setActiveScreen('battle')
        elif(selected=='chestSlot1'):
            chestOpen(1)
        elif(selected=='chestSlot2'):
            chestOpen(2)
        elif(selected=='chestSlot3'):
            chestOpen(3)
        elif(selected=='chestSlot4'):
            chestOpen(4)

def chestOpen(n):
    pass

def main_findButton(app, mouseX, mouseY):
    if(80<=mouseX<=135 and 740<=mouseY<795):
        return 'cardButton'
    elif(347.5<=mouseX<=402.5 and 740<=mouseY<=795):
        return 'shopButton'
    elif(115<=mouseX<365 and 400<=mouseY<=650):
        return 'battleButton'
    elif(15<=mouseX<=90 and 250<=mouseY<325):
        return 'settingsButton'
    elif(0<=mouseX<=120 and 580<=mouseY<=730):
        return 'chestSlot1'
    elif(120<=mouseX<=240 and 580<=mouseY<=730):
        return 'chestSlot2'
    elif(240<=mouseX<=360 and 580<=mouseY<=730):
        return 'chestSlot3'
    elif(360<=mouseX<=480 and 580<=mouseY<=730):
        return 'chestSlot4'
    return None

def cards_onScreenActivate(app):
    pass

def cards_redrawAll(app):
    drawLabel('Cards Screen', 100, 100)
    #bottom bar
    drawRect(0, 740, 480, 60, fill=rgb(67, 81, 98))
    drawRect(0, 735, 480, 5, fill=rgb(111, 137, 167))
    #battle icon
    drawImage('assets/battle_icon.png', 212.5, 740, width=55, height=55)
    drawLabel('<Battle>', 240, 790, fill='white', size=17, bold=True)
    #cards icon
    drawImage('assets/card_icon.png', 80, 740, width=55, height=55)
    #shop icon
    drawImage('assets/shop_icon.png', 347.5, 740, width=55, height=55)
    drawLabel('<Shop', 375, 790, fill='white', size=17, bold=True)
    #glow to indicate which screen
    drawRect(0, 740, 180, 60, fill=rgb(114, 145, 176), opacity=30)
    drawLabel('Cards>', 107.5, 790, fill='white', size=17, bold=True)

def cards_onKeyPress(app, key):
    if(key=='right'):
        setActiveScreen('main')

def cards_onMousePress(app, mouseX, mouseY):
    selected=shop_findButton(app, mouseX, mouseY)
    if(selected!=None):
        if(selected=='mainButton'):
            setActiveScreen('main')
        elif(selected=='shopButton'):
            setActiveScreen('shop')

def cards_findButton(app, mouseX, mouseY):
    if(80<=mouseX<=135 and 740<=mouseY<795):
        return 'shopButton'
    elif(367.5<=mouseX<=402.5 and 740<=mouseY<=795):
        return 'mainButton'
    return None

def shop_onScreenActivate(app):
    pass

def shop_redrawAll(app):
    drawLabel('Shop Screen', 240, 200, size=48, fill='black')
    #bottom bar
    drawRect(0, 740, 480, 60, fill=rgb(67, 81, 98))
    drawRect(0, 735, 480, 5, fill=rgb(111, 137, 167))
    #battle icon
    drawImage('assets/battle_icon.png', 212.5, 740, width=55, height=55)
    drawLabel('<Battle>', 240, 790, fill='white', size=17, bold=True)
    #cards icon
    drawImage('assets/card_icon.png', 80, 740, width=55, height=55)
    drawLabel('Cards>', 107.5, 790, fill='white', size=17, bold=True)
    #shop icon
    drawImage('assets/shop_icon.png', 347.5, 740, width=55, height=55)
    #glow to indicate which screen
    drawRect(300, 740, 180, 60, fill=rgb(114, 145, 176), opacity=30)
    drawLabel('<Shop', 375, 790, fill='white', size=17, bold=True)

def shop_onKeyPress(app, key):
    if(key=='left'):
        setActiveScreen('main')

def shop_onMousePress(app, mouseX, mouseY):
    selected=shop_findButton(app, mouseX, mouseY)
    if(selected!=None):
        if(selected=='mainButton'):
            setActiveScreen('main')
        elif(selected=='cardButton'):
            setActiveScreen('cards')

def shop_findButton(app, mouseX, mouseY):
    if(80<=mouseX<=135 and 740<=mouseY<795):
        return 'cardButton'
    elif(212.5<=mouseX<=267.5 and 740<=mouseY<=795):
        return 'mainButton'
    return None

def battle_onScreenActivate(app):
    #create the card library (checked working)
    Card.createCardLibrary()
    Tower.createTowerLibrary()
    #initialize the game
    app.battle = Game(app.username, 'Bot', app.deck, app.botDeck)
    app.battle.p1.elixir=7
    app.battle.p2.elixir=7
    #game time trackers
    app.steps=0
    app.constant=1
    app.gameOver=False
    #all friendly units, including towers
    app.friendlyUnits=[]
    app.enemyUnits=[]
    app.battle.shuffleStartingHands()
    #converting the cardsList into a list of card objects
    app.battle.p1.cardObjects=[Card.cardLibrary[card] for card in app.battle.p1.cards]
    app.battle.p2.cardObjects=[Card.cardLibrary[card] for card in app.battle.p2.cards]
    #vars for drawing the arena
    app.board = app.battle.createBoard()
    app.rows=len(app.board)
    app.cols=len(app.board[0])
    app.selectedCard=None
    app.selectedCell=None
    app.boardLeft=0
    app.boardTop=0
    app.boardWidth=480
    app.boardHeight=650
    app.rowHeight=app.boardHeight/app.rows
    app.colWidth=app.boardWidth/app.cols
    app.cellBorderWidth=1
    #Clones so towers dont alias to each other
    #adding Towers to app.friendlyUnits
    app.friendlyUnits.append((Tower.towerLibrary['PrincessLeft'].clone(), (3, 26)))
    app.friendlyUnits.append((Tower.towerLibrary['PrincessRight'].clone(), (14, 26)))
    app.friendlyUnits.append((Tower.towerLibrary['King'].clone(), (8.5, 29.5)))
    #adding enemy Towers to app.enemyUnits
    app.enemyUnits.append((Tower.towerLibrary['PrincessLeft'].clone(), (3, 5)))
    app.enemyUnits.append((Tower.towerLibrary['PrincessRight'].clone(), (14, 5)))
    app.enemyUnits.append((Tower.towerLibrary['King'].clone(), (8.5, 2.5)))

def battle_onStep(app):
    if(not app.gameOver):
        #elixir
        app.steps+=1
        if app.steps==7200:
            app.constant=2
        elif app.steps==10800:
            app.constant=3
        elif(app.steps)==21600:
            app.gameOver=True
        app.battle.p1.elixir=min(app.battle.p1.elixir+0.06*app.constant, 10)
        app.battle.p2.elixir=min(app.battle.p2.elixir+0.06*app.constant, 10)
        #movement
        for index, (friendlyUnit, friendlyPosition) in enumerate(app.friendlyUnits):
            if(isinstance(friendlyUnit, Tower)):
                continue
            elif(isinstance(friendlyUnit, Troop)):
                enemyTarget, enemyDistance, enemyPosition = findTarget(app, friendlyUnit)
                print(f'enemyDistance: {enemyDistance}, enemyPosition: {enemyPosition}, friendlyPosition: {friendlyPosition}')
                if(enemyDistance<=friendlyUnit.hitrange):
                    pass
                    #attackTarget(app, friendlyUnit, enemyTarget, hitspeed)
                path = getPath(app, friendlyPosition, enemyPosition, friendlyUnit)
                print(f'Path: {path}')
                if(len(path)==1):
                    pass
                    #attackTarget
                else:
                    nextRow, nextCol=path[1]
                    app.friendlyUnits[index]=(friendlyUnit, (nextCol, nextRow))
            elif(isinstance(friendlyUnit, Spell)):
                radius=friendlyUnit.radius
                for enemyUnit, enemyPosition in app.enemyUnits:
                    if(getDistance(app, friendlyUnit, enemyUnit)<=radius):
                        if(isinstance(enemyUnit, Tower)):
                            enemyUnit.health-=friendlyUnit.towerDamage
                        else:
                            enemyUnit.health-=friendlyUnit.damage
                app.friendlyUnits.pop(index)


#DO LATER: MAKE TARGETTING SPECIFIC; CURRENTLY ALL TROOPS TARGET EACH OTHER
def findTarget(app, unit):
    #unitTarget=unit.targets
    closestTarget=None
    closestDistance=None
    closestPosition=None
    #movementVector=None
    for enemyUnit, enemyPosition in app.enemyUnits:
        currDistance = getDistance(app, unit, enemyUnit)
        if(closestTarget==None or currDistance<closestDistance):
            closestTarget=enemyUnit
            closestDistance=currDistance
            closestPosition=enemyPosition
    return closestTarget, closestDistance, closestPosition
  
def getPath(app, start, end, unit):
    startCol, startRow = start
    endCol, endRow = end
    newStart = startRow, startCol
    newEnd = endRow, endCol
    hitrange=unit.hitrange
    return astar(app.board, newStart, newEnd, hitrange)

def findIndex(app, unit, friendTF):
    #where u and p represent unit, position
    unitList=[]
    positionList=[]
    if(friendTF):
        for u, p in app.friendlyUnits:
            unitList.append(u)
            positionList.append(p)
    else:
        for u, p in app.enemyUnits:
            unitList.append(u)
            positionList.append(p)
    return unitList.index(unit)

def getDistance(app, friendlyUnit, enemyUnit):
    friendlyIndex=findIndex(app, friendlyUnit, True)
    friendC, friendR=app.friendlyUnits[friendlyIndex][1]
    enemyIndex=findIndex(app, enemyUnit, False)
    enemyC, enemyR=app.enemyUnits[enemyIndex][1]
    #print(f'enemyC, enemyR = {enemyC, enemyR}')
    diffC, diffR =(enemyC-friendC), (enemyR-friendR)
    #print(f'diffC, diffR: {diffC, diffR}')
    return math.sqrt(diffC**2 + diffR**2)

def attackTarget():
    pass

def battle_redrawAll(app):
    #the background for the card deck in game
    drawImage('assets/woodbg.png', 0, 650, width=480, height=150, opacity=85)
    #drawing the elixir bar and the lines
    drawRect(40, 755, 430 * app.battle.p1.elixir/10, 40, fill=rgb(194, 33, 199))
    drawRect(40, 755, 430, 40, fill=None, border='black', borderWidth=2)
    #1-10 for the 10 elixir bars, 40 is the starting x coordinate, 43 is by 430/10 from the above line
    for n in range(1, 10):
        drawLine(40+43*n, 755, 40+43*n, 795, lineWidth=2)
    drawImage('assets/elixir_icon.png', 0, 745, width=60, height=60)
    drawLabel(math.floor(app.battle.p1.elixir), 30, 775, fill='white', size=24, bold=True)
    #drawing the empty card slots that will be set to cards
    drawRect(90, 660, 75, 90, fill=rgb(95, 66, 50))
    drawRect(175, 660, 75, 90, fill=rgb(95, 66, 50))
    drawRect(260, 660, 75, 90, fill=rgb(95, 66, 50))
    drawRect(345, 660, 75, 90, fill=rgb(95, 66, 50))
    #filling the slots with cards
    drawImage(app.battle.p1.cardObjects[0].image, 90, 660, width=75, height=90)
    drawImage(app.battle.p1.cardObjects[1].image, 175, 660, width=75, height=90)
    drawImage(app.battle.p1.cardObjects[2].image, 260, 660, width=75, height=90)
    drawImage(app.battle.p1.cardObjects[3].image, 345, 660, width=75, height=90)
    #drawing the next card
    drawRect(5, 705, 35, 45, fill=rgb(95, 66, 50))
    drawImage(app.battle.p1.cardObjects[4].image, 5, 705, width=35, height=45)
    drawLabel('Next:', 20, 700, fill='white', size=16, bold=True)
    #creating the board
    for row in range(app.rows):
        for col in range(app.cols):
            if((col, row)==app.selectedCell):
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill='white', opacity=50)
            else:
                drawCell(app, row, col)
    #drawing the red towers
    drawImage('assets/red_princess_tower.png', 53, 80, width=80, height=70)
    drawImage('assets/red_princess_tower.png', 347, 80, width=80, height=70)
    drawImage('assets/red_king_tower.png', 187, 0, width=106, height=81)
    #drawing the blue towers
    drawImage('assets/red_princess_tower.png', 53, 508, width=80, height=70)
    drawImage('assets/red_princess_tower.png', 347, 508, width=80, height=70)
    drawImage('assets/blue_king_tower.png', 187, 569, width=106, height=81)
    #drawing the units/buildings in friendlyUnits
    for friendlyUnit, friendlyPosition in app.friendlyUnits:
        if(isinstance(friendlyUnit, (Troop, Building, Tower))):
            drawUnit(app, friendlyUnit, friendlyPosition)
    #repeating for enemy units
    for enemyUnit, enemyPosition in app.enemyUnits:
        if(isinstance(friendlyUnit, (Troop, Building, Tower))):
            drawUnit(app, enemyUnit, enemyPosition) 
    #drawing timer
    drawTimer(app)  

def drawUnit(app, unit, position):
    col, row = position
    colRatio, rowRatio = col/app.cols, row/app.rows
    adjustedX=colRatio*app.boardWidth+(app.colWidth/2)
    adjustedY=rowRatio*app.boardHeight-(app.rowHeight/2)
    if(isinstance(unit, (Troop, Building))):
        drawImage(unit.sprite, adjustedX, adjustedY, align='center')
    drawLabel(unit.health, adjustedX, adjustedY, size=18, fill='white', bold=True)

def drawTimer(app):
    seconds = app.steps//app.stepsPerSecond
    minutes = seconds//60
    seconds -= minutes*60
    secondsString=f'0{seconds}' if(seconds<10) else str(seconds)
    minutesString=f'0{minutes}' if(minutes<10) else str(minutes)
    time = f'{minutesString}:{secondsString}'
    drawLabel(time, 440, 20, fill='white', size=24, bold=True)

def drawCell(app, row, col):
    colorList=['green', 'blue', 'brown', 'black', 'red']
    colorIndex=app.board[row][col]
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=colorList[colorIndex], border='black', borderWidth=app.cellBorderWidth)
    
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def battle_onKeyPress(app, key):
    if(key=='escape'):
        setActiveScreen('main')
    elif(key=='1'):
        app.selectedCard=app.battle.p1.cardObjects[0]
        print('Selected Card:', app.selectedCard.name)
    elif(key=='2'):
        app.selectedCard=app.battle.p1.cardObjects[1]
        print('Selected Card:', app.selectedCard.name)
    elif(key=='3'):
        app.selectedCard=app.battle.p1.cardObjects[2]
        print('Selected Card:', app.selectedCard.name)
    elif(key=='4'):
        app.selectedCard=app.battle.p1.cardObjects[3]
        print('Selected Card:', app.selectedCard.name)

def battle_onMouseMove(app, mouseX, mouseY):
    app.selectedCell=battle_getCell(app, mouseX, mouseY)        

def battle_onMousePress(app, mouseX, mouseY):
    selectedCell=battle_getCell(app, mouseX, mouseY)
    print(selectedCell)
    if(app.selectedCard!=None):
        selectedIndex=app.battle.p1.cards.index(app.selectedCard.name)
        if(selectedCell!=None):
            print(selectedCell, app.selectedCard.name)
            if(validPosition(app, app.selectedCard, selectedCell)):
                #print('Valid Position!')
                app.battle.p1.deployCard(app, app.selectedCard, selectedCell, selectedIndex)
                #print(f'friendlyUnits: {app.friendlyUnits}')
            else:
                print('Invalid Position!')
            
def validPosition(app, selectedCard, selectedCell):
    cardType = type(selectedCard)
    selectedCol, selectedRow = selectedCell
    if(cardType==Troop):
        return selectedRow>15 and app.board[selectedRow][selectedCol]==0
    elif(cardType==Building):
        return selectedRow>15 and app.board[selectedRow][selectedCol]==0
    elif(cardType==Spell):
        return True

#returns the format as (x, y) or (col, row)
def battle_getCell(app, mouseX, mouseY):
    if(mouseX>480 or mouseY>650):
        return None
    else:
        cellWidth=app.boardWidth/app.cols
        cellHeight=app.boardHeight/app.rows
        return math.floor(mouseX/cellWidth), math.floor(mouseY/cellHeight)


def settings_onScreenActivate(app):
    pass

def settings_redrawAll(app):
    pass

def main():
    runAppWithScreens(initialScreen='main');

main()
