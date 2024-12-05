from cmu_graphics import *
from game import Game
from entity import Card, Building, Troop, Spell, Tower, PrincessLeft, PrincessRight, King
from node import Node, astar
import math, copy, random, time

#Jack Xie, jackx2
#This project in its entirety, the concepts, the sprites, etc. are taken from Supercell's game Clash Royale.
#All sprites can be found at https://github.com/smlbiobot/cr-assets-png/tree/master/assets
#Any other uncited images are from in game screenshots from Supercell's game Clash Royale
#This project is meant to mimic some of the core features of Clash Royale
#TODO:
#1. make A* work on air units, add the attribute targetting so tower doenst retarget to closest target if troop walks in front of another
#2. make sure the targetting system works, no way to test currently (also fix pathing issue with range of giant/minipekka)
#3. Imrpove UI, comment code (A*, timer, @classmethod), etc.
#5. get the font to work
#6. Fix bug with destroying king tower, also when both towers destroyed, pathing is weird
#7. make valid position work
def onAppStart(app):
    app.stepsPerSecond=1000
    app.width=480
    app.height=800
    app.gold=0
    app.gems=0
    app.experience=0
    app.username='User'
    app.botDeck=['Archers', 'Archers', 'Archers', 'Archers', 'Archers', 'Archers', 'Archers', 'Archers']
    app.deck=['Archers', 'Knight', 'Giant', 'Fireball', 'Arrows', 'Cannon', 'Mini-Pekka', 'Musketeer']
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
    drawLabel(f'Welcome, {app.username}!', 240, 120, size=48, fill='white', bold=True)
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
    drawLabel('<FAQ', 375, 790, fill='white', size=17, bold=True)
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
    #time constants
    app.initialTime=time.time()
    app.previousTime=app.initialTime
    app.dt=None
    app.countdownTime=360
    app.remainingTime=app.countdownTime-app.initialTime
    #create the card library (checked working)
    Card.createCardLibrary()
    Tower.createTowerLibrary()
    #initialize the game
    app.battle = Game(app.username, 'Bot', app.deck, app.botDeck)
    app.battle.p1.elixir=5
    app.battle.p2.elixir=5
    #game time trackers
    app.steps=0
    app.constant=1
    app.gameOver=False
    #all friendly units, including towers
    app.friendlyUnits=[]
    app.enemyUnits=[]
    app.battle.shuffleStartingHands()
    #getting the lists of cards
    app.battle.p1.cards=app.deck
    app.battle.p2.cards=app.botDeck
    #converting the cardsList into a list of card objects
    app.battle.p1.cardObjects=[Card.cardLibrary[card] for card in app.battle.p1.cards]
    app.battle.p2.cardObjects=[Card.cardLibrary[card] for card in app.battle.p2.cards]
    #vars for drawing the arena
    app.board = app.battle.createBoard()
    app.rows=len(app.board)
    app.cols=len(app.board[0])
    app.friendlySelectedCard=None
    app.enemySelectedCard=None
    app.friendlySelectedCell=None
    app.enemySelectedCell=None
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
    #deck colors
    app.card1bg=rgb(95, 66, 50)
    app.card2bg=rgb(95, 66, 50)
    app.card3bg=rgb(95, 66, 50)
    app.card4bg=rgb(95, 66, 50)

def battle_onStep(app):
    if(app.gameOver):
        setActiveScreen('main')
    else:
        #time
        app.currentTime=time.time()
        elapsedTime=app.currentTime-app.initialTime
        app.dt=app.currentTime-app.previousTime
        app.previousTime=app.currentTime
        app.remainingTime=max(0, app.countdownTime-elapsedTime)
        #elixir
        if math.floor(app.remainingTime)>240:
            app.constant=1
        elif math.floor(app.remainingTime>180):
            app.constant=2
        elif math.floor(app.remainingTime>0):
            app.constant=3
        elif app.remainingTime==0:
            app.gameOver=True
        elixirRate=1/2.8
        app.battle.p1.elixir=min(app.battle.p1.elixir+app.dt*elixirRate*app.constant, 10)
        app.battle.p2.elixir=min(app.battle.p2.elixir+app.dt*elixirRate*app.constant, 10)
        #enemy bot moves
        enemyPlaceCard(app)
        #checking towers and adjusting removing unwalkable black/red squares
        updateBoard(app)
        #making units move/attack
        processUnits(app, app.friendlyUnits, app.enemyUnits)
        processUnits(app,app.enemyUnits, app.friendlyUnits)

def updateBoard(app):
    rowColIndices=[(25, 28, 2, 5), (25, 28, 13, 16), (28, 32, 7, 11), (4, 7, 2, 5), (4, 7, 13, 16), (0, 4, 7, 11)]
    friendlyLeft, friendlyRight, friendlyKing = checkTowers(app.friendlyUnits)
    enemyLeft, enemyRight, enemyKing = checkTowers(app.enemyUnits)
    #if tower is destroyed, remove the black/red squares
    for index, status in enumerate((friendlyLeft, friendlyRight, friendlyKing, enemyLeft, enemyRight, enemyKing)):
        if(status==None):
            staticSetSquare(app.board, *rowColIndices[index], 0)

def staticSetSquare(board, sRow, eRow, sCol, eCol, n):
        for row in range(sRow, eRow):
            for col in range(sCol, eCol):
                board[row][col]=n

def processUnits(app, friendlyUnits, enemyUnits):
    clearUnits(friendlyUnits)
    for friendlyIndex, (friendlyUnit, friendlyPosition) in enumerate(friendlyUnits):
            if(isinstance(friendlyUnit, Tower)):
                #for King towers, check if any princesses are destroyed or if health isnt full
                #if king not active, just skip dont do anything
                if(isinstance(friendlyUnit, King)):
                    if(None in checkTowers(friendlyUnits) or friendlyUnit.health!=4824):
                        friendlyUnit.active=True
                    if(not friendlyUnit.active):
                        continue
                if(friendlyUnit.targeting==None):
                    enemyTarget, enemyDistance, enemyPosition, enemyIndex = friendlyUnit.findTarget(friendlyPosition, enemyUnits)
                    if(enemyDistance<=friendlyUnit.hitrange):
                        friendlyUnit.attackTarget(app, enemyTarget, enemyIndex, enemyUnits)
                else:
                    friendlyUnit.attackTarget(app, *friendlyUnit.targeting)
            elif(isinstance(friendlyUnit, Troop)):
                if(friendlyUnit.targeting==None):
                    enemyTarget, enemyDistance, enemyPosition, enemyIndex = friendlyUnit.findTarget(friendlyPosition, enemyUnits)
                    #print(f'enemyDistance: {enemyDistance}, enemyPosition: {enemyPosition}, friendlyPosition: {friendlyPosition}')
                    friendlyCol, friendlyRow = friendlyPosition
                    enemyCol, enemyRow = enemyPosition
                    path = getPath(app, (math.floor(friendlyCol), math.floor(friendlyRow)), (math.floor(enemyCol), math.floor(enemyRow)), friendlyUnit)
                    #print(f'Path: {path}')
                    if(len(path)==1):
                        friendlyUnit.attackTarget(app, enemyTarget, enemyIndex, enemyUnits)
                    else:
                        nextRow, nextCol=path[1]
                        newPosition=friendlyUnit.move(app, friendlyPosition, nextRow, nextCol)
                        friendlyUnits[friendlyIndex]=(friendlyUnit, newPosition)
                else:
                    friendlyUnit.attackTarget(app, *friendlyUnit.targeting)
            elif(isinstance(friendlyUnit, Spell)):
                #List of all indices that need to be popped
                poppingIndices=[]
                radius=friendlyUnit.radius
                for enemyIndex, (enemyUnit, enemyPosition) in enumerate(enemyUnits):
                    if(friendlyUnit.getDistance(friendlyPosition, enemyPosition)<=radius):
                        #print('HERE')
                        if(isinstance(enemyUnit, Tower)):
                            enemyUnit.health=max(0, enemyUnit.health-friendlyUnit.towerDamage)
                        else:
                            enemyUnit.health=max(0, enemyUnit.health-friendlyUnit.damage)
                        if(enemyUnit.health<=0):
                            if isinstance(enemyUnit, King):
                                app.gameOver=True
                                continue
                            poppingIndices.append(enemyIndex)
                enemyUnits=popFromIndices(enemyUnits, poppingIndices)
                friendlyUnits.pop(friendlyIndex)
            elif(isinstance(friendlyUnit, Building)):
                if(friendlyUnit.targeting==None):
                    friendlyUnit.health-=(app.dt/friendlyUnit.lifespan)*friendlyUnit.initialHealth
                    enemyTarget, enemyDistance, enemyPosition, enemyIndex = friendlyUnit.findTarget(friendlyPosition, enemyUnits)
                    if(enemyDistance<=friendlyUnit.hitrange):
                        friendlyUnit.attackTarget(app, enemyTarget, enemyIndex, enemyUnits)
                else:
                    friendlyUnit.attackTarget(app, *friendlyUnit.targeting)

def popFromIndices(L, indices):
    #where L is the original list and indices contains the indices to be popped
    L=copy.deepcopy(L)
    indices = sorted(indices, reverse=True)
    for index in indices:
        L.pop(index)
    return L

def clearUnits(unitsList):
    for index, (unit, position) in enumerate(unitsList):
        if(not isinstance(unit, Spell) and unit.health<=0):
            unitsList.pop(index)

def getPath(app, start, end, unit):
    startCol, startRow = start
    endCol, endRow = end
    newStart = startRow, startCol
    newEnd = endRow, endCol
    hitrange=unit.hitrange
    targetted=unit.targetted
    return astar(app.board, newStart, newEnd, hitrange, targetted)

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
    #letting user know if elixir is full
    if(app.battle.p1.elixir==10):
        drawLabel('Elixir is full!', 240, 775, fill='red', size=24, bold=True)    
    drawLabel(math.floor(app.battle.p1.elixir), 30, 775, fill='white', size=24, bold=True)
    #drawing the empty card slots that will be set to cards
    drawRect(90, 660, 75, 90, fill=app.card1bg)
    drawRect(175, 660, 75, 90, fill=app.card2bg)
    drawRect(260, 660, 75, 90, fill=app.card3bg)
    drawRect(345, 660, 75, 90, fill=app.card4bg)
    #filling the slots with cards
    drawImage(app.battle.p1.cardObjects[0].image, 90, 660, width=75, height=90)
    drawImage(app.battle.p1.cardObjects[1].image, 175, 660, width=75, height=90)
    drawImage(app.battle.p1.cardObjects[2].image, 260, 660, width=75, height=90)
    drawImage(app.battle.p1.cardObjects[3].image, 345, 660, width=75, height=90)
    #drawing the elixir costs for each card 
    drawImage('assets/elixir_icon.png', 115, 730, width=25, height=25)
    drawImage('assets/elixir_icon.png', 200, 730, width=25, height=25)
    drawImage('assets/elixir_icon.png', 285, 730, width=25, height=25)
    drawImage('assets/elixir_icon.png', 370, 730, width=25, height=25)
    drawLabel(app.battle.p1.cardObjects[0].cost, 127.5, 742.5, fill='white', bold=True)
    drawLabel(app.battle.p1.cardObjects[1].cost, 212.5, 742.5, fill='white', bold=True)
    drawLabel(app.battle.p1.cardObjects[2].cost, 297.5, 742.5, fill='white', bold=True)
    drawLabel(app.battle.p1.cardObjects[3].cost, 382.5, 742.5, fill='white', bold=True)
    #drawing the next card
    drawRect(5, 705, 35, 45, fill=rgb(95, 66, 50))
    drawImage(app.battle.p1.cardObjects[4].image, 5, 705, width=35, height=45)
    drawLabel('Next:', 20, 700, fill='white', size=16, bold=True)
    #creating the board
    for row in range(app.rows):
        for col in range(app.cols):
            if((col, row)==app.friendlySelectedCell):
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill='white', opacity=50)
            else:
                drawCell(app, row, col)
    #drawing the depoyable squares over the board
    if(app.friendlySelectedCard!=None):
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                if(friendlyValidPosition(app, app.friendlySelectedCard, (col, row))):
                    cellleft, cellTop = getCellLeftTop(app, row, col)
                    cellWidth, cellHeight = getCellSize(app)
                    drawRect(cellleft, cellTop, cellWidth, cellHeight, fill='red', opacity=20)
    #drawing the red towers
    enemyLeft, enemyRight, enemyKing = checkTowers(app.enemyUnits)
    if(enemyLeft):
        drawImage('assets/red_princess_tower.png', 53, 80, width=80, height=70)
    if(enemyRight):
        drawImage('assets/red_princess_tower.png', 347, 80, width=80, height=70)
    if(enemyKing):
        drawImage('assets/red_king_tower.png', 187, 0, width=106, height=81)
    #drawing the blue towers
    friendlyLeft, friendlyRight, friendlyKing = checkTowers(app.friendlyUnits)
    if(friendlyLeft):
        drawImage('assets/red_princess_tower.png', 53, 508, width=80, height=70)
    if(friendlyRight):
        drawImage('assets/red_princess_tower.png', 347, 508, width=80, height=70)
    if(friendlyKing):
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
    #drawing spell range if selected card is Spell
    drawSpellBorders(app)

def checkTowers(friendlyList):
    left, right, king = None, None, None
    for unit, position in friendlyList:
        if isinstance(unit, PrincessLeft):
            left=True
        elif(isinstance(unit, PrincessRight)):
            right=True
        elif(isinstance(unit, King)):
            king=True
    return left, right, king

def drawSpellBorders(app):
    if(isinstance(app.friendlySelectedCard, Spell) and app.friendlySelectedCell!=None):
        radius=app.friendlySelectedCard.radius
        col, row = app.friendlySelectedCell
        adjustedX, adjustedY = cellToPixel(app, row, col)
        if(app.friendlySelectedCell!=None):
            drawOval(adjustedX, adjustedY, radius*app.colWidth*2, radius*app.rowHeight*2, fill='white', opacity=25)

def cellToPixel(app, row, col):
    adjustedX = (col+0.5)*app.colWidth
    adjustedY = (row+0.5)*app.rowHeight
    return adjustedX, adjustedY

def drawUnit(app, unit, position):
    col, row = position
    adjustedX, adjustedY = cellToPixel(app, row, col)
    if(isinstance(unit, (Troop, Building))):
        drawImage(unit.sprite, adjustedX, adjustedY, align='center')
    drawLabel(rounded(unit.health), adjustedX, adjustedY, size=18, fill='white', bold=True)

def rounded(n):
    return math.floor(n+0.5) if n>0 else math.floor(n-0.5)

def drawTimer(app):
    seconds = math.floor(app.remainingTime)
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
        app.friendlySelectedCard=app.battle.p1.cardObjects[0]
        app.card1bg='white'
        app.card2bg=rgb(95, 66, 50)
        app.card3bg=rgb(95, 66, 50)
        app.card4bg=rgb(95, 66, 50)
        print('Selected Card:', app.friendlySelectedCard.name)
    elif(key=='2'):
        app.friendlySelectedCard=app.battle.p1.cardObjects[1]
        app.card2bg='white'
        app.card1bg=rgb(95, 66, 50)
        app.card3bg=rgb(95, 66, 50)
        app.card4bg=rgb(95, 66, 50)        
        print('Selected Card:', app.friendlySelectedCard.name)
    elif(key=='3'):
        app.friendlySelectedCard=app.battle.p1.cardObjects[2]
        app.card3bg='white'
        app.card1bg=rgb(95, 66, 50)
        app.card2bg=rgb(95, 66, 50)
        app.card4bg=rgb(95, 66, 50)
        print('Selected Card:', app.friendlySelectedCard.name)
    elif(key=='4'):
        app.friendlySelectedCard=app.battle.p1.cardObjects[3]
        app.card4bg='white'
        app.card1bg=rgb(95, 66, 50)
        app.card2bg=rgb(95, 66, 50)
        app.card3bg=rgb(95, 66, 50)
        print('Selected Card:', app.friendlySelectedCard.name)

def battle_onMouseMove(app, mouseX, mouseY):
    app.friendlySelectedCell=battle_getCell(app, mouseX, mouseY)

def battle_onMousePress(app, mouseX, mouseY):
    selectedCell=battle_getCell(app, mouseX, mouseY)
    print(selectedCell)
    if(selectedCell==None):
        if(90<=mouseX<=165 and 660<=mouseY<=750):
            app.friendlySelectedCard=app.battle.p1.cardObjects[0]
            app.card1bg='white'
            app.card2bg=rgb(95, 66, 50)
            app.card3bg=rgb(95, 66, 50)
            app.card4bg=rgb(95, 66, 50)
            print('Selected Card:', app.friendlySelectedCard.name) 
        elif(175<=mouseX<=250 and 660<=mouseY<=750):
            app.friendlySelectedCard=app.battle.p1.cardObjects[1]
            app.card2bg='white'
            app.card1bg=rgb(95, 66, 50)
            app.card3bg=rgb(95, 66, 50)
            app.card4bg=rgb(95, 66, 50)
            print('Selected Card:', app.friendlySelectedCard.name) 
        elif(260<=mouseX<=335 and 660<=mouseY<=750):
            app.friendlySelectedCard=app.battle.p1.cardObjects[2]
            app.card3bg='white'
            app.card1bg=rgb(95, 66, 50)
            app.card2bg=rgb(95, 66, 50)
            app.card4bg=rgb(95, 66, 50)
            print('Selected Card:', app.friendlySelectedCard.name)
        elif(345<=mouseX<=420 and 660<=mouseY<=750):
            app.friendlySelectedCard=app.battle.p1.cardObjects[3]
            app.card4bg='white'
            app.card1bg=rgb(95, 66, 50)
            app.card2bg=rgb(95, 66, 50)
            app.card3bg=rgb(95, 66, 50)
            print('Selected Card:', app.friendlySelectedCard.name) 
    if(app.friendlySelectedCard!=None):
        selectedIndex=app.battle.p1.cards.index(app.friendlySelectedCard.name)
        if(selectedCell!=None):
            print(selectedCell, app.friendlySelectedCard.name)
            if(friendlyValidPosition(app, app.friendlySelectedCard, selectedCell)):
                #print('Valid Position!')
                app.battle.p1.deployCard(app, app.friendlySelectedCard, selectedCell, selectedIndex, app.friendlyUnits, app.friendlySelectedCard)
                app.friendlySelectedCard=None
                #print(f'friendlyUnits: {app.friendlyUnits}')
            else:
                print('Invalid Position!')
            
def friendlyValidPosition(app, selectedCard, selectedCell):
    cardType = type(selectedCard)
    selectedCol, selectedRow = selectedCell
    left, right, king = checkTowers(app.enemyUnits)
    if(cardType==Spell):
        return True
    elif(cardType==Troop or cardType==Building):
        if(app.board[selectedRow][selectedCol] in [0, 2]):
            if(selectedRow>16):
                return True
            if(left==None):
                return selectedRow>7 and selectedCol<=9
            if(right==None):
                return selectedRow>7 and selectedCol>=9

def enemyValidPosition(app, selectedCard, selectedCell):
    cardType = type(selectedCard)
    selectedCol, selectedRow = selectedCell
    left, right, king = checkTowers(app.friendlyUnits)
    if(cardType==Spell):
        return True
    elif(cardType==Troop or cardType==Building):
        if(app.board[selectedRow][selectedCol] in [0, 2]):
            if(selectedRow<15):
                return True
            if(left==None):
                return selectedRow<24 and selectedCol<=9
            if(right==None):
                return selectedRow<24 and selectedCol>=9

def enemyPlaceCard(app):
    #currently only deploys archers at constant time intervals
    app.enemySelectedCard=app.battle.p2.cardObjects[0]
    app.battle.p2.deployCard(app, app.enemySelectedCard, (8, 8), 0, app.enemyUnits, app.enemySelectedCard)

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
    drawImage('assets/bg.png', 0, 0)
    drawLabel('Settings', 240, 40, fill='white', size=48, bold=True)
    drawLabel('(press escape to return)', 240, 75, fill='white', size=12)


def settings_onKeyPress(app, key):
    if(key=='escape'):
        setActiveScreen('main')

def main():
    runAppWithScreens(initialScreen='main');

main()
