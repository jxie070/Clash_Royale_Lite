from cmu_graphics import *
from game import Game
from entity import Card, Building, Troop, Spell, Tower, PrincessLeft, PrincessRight, King
from node import Node, astar
from player import Player
import math, copy, random, time, string

#Jack Xie, jackx2
#This project in its entirety, the concepts, the sprites, etc. are taken from Supercell's game Clash Royale.
#All sprites can be found at https://github.com/smlbiobot/cr-assets-png/tree/master/assets
#Any other uncited images are from in game screenshots from Supercell's game Clash Royale
#This project is meant to mimic some of the core features of Clash Royale
def onAppStart(app):
    app.stepsPerSecond=1000
    app.width=480
    app.height=800
    app.gold=0
    app.gems=0
    app.experience=0
    app.username='User'
    app.botDeck=['Archers', 'Knight', 'Giant', 'Mini-Pekka', 'Archers', 'Knight', 'Giant', 'Mini-Pekka']
    app.deck=['Archers', 'Knight', 'Giant', 'Fireball', 'Arrows', 'Cannon', 'Mini-Pekka', 'Musketeer']
    app.font='supercell-magic'
    #create the card library
    Card.createCardLibrary()
    Tower.createTowerLibrary()
    #music vars
    app.music=True
    app.sfx=True
    app.menuMusic=Sound('sounds/menu.wav')
    app.tapSound=Sound('sounds/tap.wav')
    app.winSound=Sound('sounds/win.wav')
    app.lossSound=Sound('sounds/loss.wav')
    app.drawSound=Sound('sounds/draw.wav')
    app.battleMusic=Sound('sounds/battle.wav')
    app.menuMusic.play(restart=False, loop=True)

def main_redrawAll(app):
    #on main start is on app start
    #background
    drawImage('assets/bg.png', 0, 0)
    #gui
    drawImage('assets/battle_button.png', 115, 400, width=250, height=250)
    drawLabel('Battle', 240, 525, fill='white', size=32, bold=True, border='black', font=app.font, borderWidth=2)
    drawImage('assets/arena.png', 80, 140, width=290, height=320)
    drawRect(0, 8, 480, 52, fill=rgb(4, 21, 45), opacity=75)
    drawImage('assets/gem_icon.png', 420, 10, width=50, height=50)
    drawLabel(app.gems, 420, 35, size=24, font=app.font, bold=True, fill='white', align='right')
    drawImage('assets/gold_icon.png', 280, 10, width=50, height=50)
    drawLabel(app.gold, 275, 35, size=24, font=app.font, bold=True, fill='white', align='right')
    drawImage('assets/experience_icon.png', 10, 12, width=40, height=40)
    drawLabel(app.experience, 60, 35, size=24, font=app.font, bold=True, fill='white', align='left')
    drawImage('assets/settings_icon.png', 15, 250, width=75, height=75)
    drawLabel(f'Welcome, {app.username}!', 240, 120, size=24, font=app.font, fill='white', bold=True)
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
    drawLabel('Cards>', 107.5, 790, font=app.font, fill='white', size=17, bold=True)
    #shop icon
    drawImage('assets/shop_icon.png', 347.5, 740, width=55, height=55)
    drawLabel('<FAQ', 375, 790, font=app.font, fill='white', size=17, bold=True)
    #glow to indicate which screen
    drawRect(180, 740, 120, 60, fill=rgb(114, 145, 176), opacity=30)
    #battle icon
    drawImage('assets/battle_icon.png', 212.5, 740, width=55, height=55)
    drawLabel('<Battle>', 240, 790, font=app.font, fill='white', size=20, bold=True)   

#when on main screen, pressing left should go to cards; pressing right should go to shop
def main_onKeyPress(app, key):
    if(app.sfx and key in ['left', 'right']):
        app.tapSound.play()
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
            app.menuMusic.pause()
            setActiveScreen('battle')
        elif(selected=='chestSlot1'):
            chestOpen(1)
        elif(selected=='chestSlot2'):
            chestOpen(2)
        elif(selected=='chestSlot3'):
            chestOpen(3)
        elif(selected=='chestSlot4'):
            chestOpen(4)
    if(app.sfx and selected!=None):
        app.tapSound.play()

def chestOpen(n):
    #unimplemented feature :(
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
    app.selectedCard=None
    app.player = Player(app.username, app.deck)
    app.player.cardObjects = [Card.cardLibrary[card] for card in app.player.cards]

def cards_redrawAll(app):
    drawImage('assets/bg.png', 0, 0)
    drawLabel('Cards Screen', 100, 100)
    #bottom bar
    drawRect(0, 740, 480, 60, fill=rgb(67, 81, 98))
    drawRect(0, 735, 480, 5, fill=rgb(111, 137, 167))
    #battle icon
    drawImage('assets/battle_icon.png', 212.5, 740, width=55, height=55)
    drawLabel('<Battle>', 240, 790, font=app.font, fill='white', size=17, bold=True)
    #cards icon
    drawImage('assets/card_icon.png', 80, 740, width=55, height=55)
    #shop icon
    drawImage('assets/shop_icon.png', 347.5, 740, width=55, height=55)
    drawLabel('<FAQ', 375, 790, font=app.font, fill='white', size=17, bold=True)
    #glow to indicate which screen
    drawRect(0, 740, 180, 60, fill=rgb(114, 145, 176), opacity=30)
    drawLabel('Cards>', 107.5, 790, font=app.font, fill='white', size=20, bold=True)
    #wooden background
    drawImage('assets/woodbg.png', 0, 0, width=480, height=280)
    #drawing in the cards and the elixir costs
    cardSpace=90
    leftSpace=70
    elixirSpace=20
    for i in range(4):
        drawRect(leftSpace+cardSpace*i, 20, 70, 90, fill=rgb(95, 66, 50))
        drawImage(app.player.cardObjects[i].image, leftSpace+cardSpace*i, 20, width=70, height=90)
        drawImage('assets/elixir_icon.png', leftSpace+cardSpace*i-elixirSpace, 10, width=40, height=40)
        drawLabel(app.player.cardObjects[i].cost, leftSpace+cardSpace*i, 30, font=app.font, fill='white', size=12)
    for j in range(4, 8):
        drawRect(leftSpace+(j-4)*cardSpace, 130, 70, 90, fill=rgb(95, 66, 50))
        drawImage(app.player.cardObjects[j].image, leftSpace+(j-4)*cardSpace, 130, width=70, height=90)
        drawImage('assets/elixir_icon.png', leftSpace+cardSpace*(j-4)-elixirSpace, 120, width=40, height=40)
        drawLabel(app.player.cardObjects[j].cost, leftSpace+cardSpace*(j-4), 140, font=app.font, fill='white', size=12)
        drawRect(0, 230, 480, 50, fill=rgb(95, 66, 50))
        drawLabel(f'Average Elixir Cost: {getAverageElixir(app.player.cardObjects)}', 240, 255, font=app.font, size=18, fill='white')
    #drawing the card stats
    drawRect(0, 280, 480, 460, fill=rgb(39, 41, 43))
    if(app.selectedCard==None):
        drawLabel('(Use keys 1-8 to select a card)', 240, 300, font=app.font, size=18, fill='white')
        drawLabel('Press 0 to return to this screen)', 240, 350, font=app.font, size=18, fill='white')
    else:
        drawRect(20, 350, 140, 180, fill=rgb(95, 66, 50))
        drawImage(app.selectedCard.image, 20, 350, width=140, height=180)
        drawLabel(app.selectedCard.name, 90, 330, font=app.font, size=16, fill='white')
        drawImage('assets/damage.png', 170, 350, width=40, height=40)
        drawLabel(f'Damage: {app.selectedCard.damage}', 215, 370, fill='white', font=app.font, size=16, align='left')
        if(isinstance(app.selectedCard, Troop)):
            drawLabel('Class: Troop', 90, 540, font=app.font, size=16, fill='white')
            drawImage('assets/hp.png', 170, 400, width=40, height=40)
            drawLabel(f'Hitpoints: {app.selectedCard.health}', 215, 420, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/hitspeed.png', 170, 450, width=40, height=40)
            drawLabel(f'Hit Speed: {app.selectedCard.hitspeed}s', 215, 470, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/hitrange.png', 170, 500, width=40, height=40)
            drawLabel(f'Range: {app.selectedCard.hitrange} tiles', 215, 520, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/speed.png', 170, 550, width=40, height=40)
            drawLabel(f'Speed: {app.selectedCard.speed}', 215, 570, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/targets.png', 170, 600, width=40, height=40)
            drawLabel(f'Targets: {', '.join(app.selectedCard.targets)}', 215, 620, fill='white', font=app.font, size=16, align='left')
            if(app.selectedCard.count>1):
                drawImage('assets/count.png', 170, 650, width=40, height=40)
                drawLabel(f'Count: {app.selectedCard.count}x', 215, 670, fill='white', font=app.font, size=16, align='left')
        elif(isinstance(app.selectedCard, Spell)):
            drawLabel('Class: Spell', 90, 540, font=app.font, size=16, fill='white')
            drawImage('assets/tower_damage.png', 170, 400, width=40, height=40)
            drawLabel(f'Tower Damage: {app.selectedCard.towerDamage}', 215, 420, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/radius.png', 170, 450, width=40, height=40)
            drawLabel(f'Spell Radius: {app.selectedCard.radius} tiles', 215, 470, fill='white', font=app.font, size=16, align='left')
        elif(isinstance(app.selectedCard, Building)):
            drawLabel('Class: Building', 90, 540, font=app.font, size=16, fill='white')
            drawImage('assets/hp.png', 170, 400, width=40, height=40)
            drawLabel(f'Hitpoints: {app.selectedCard.initialHealth}', 215, 420, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/hitspeed.png', 170, 450, width=40, height=40)
            drawLabel(f'Hit Speed: {app.selectedCard.hitspeed}s', 215, 470, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/hitrange.png', 170, 500, width=40, height=40)
            drawLabel(f'Range: {app.selectedCard.hitrange} tiles', 215, 520, fill='white', font=app.font, size=16, align='left')
            drawImage('assets/lifespan.png', 170, 550, width=40, height=40)
            drawLabel(f'Duration: {app.selectedCard.lifespan}s', 215, 570, fill='white', font=app.font, size=16, align='left')

def getAverageElixir(cardObjects):
    total=0
    numCards=0
    for card in cardObjects:
        numCards+=1
        total+=card.cost
    return pythonRound(total/numCards, 1)

def cards_onKeyPress(app, key):
    if(app.sfx and key in ['right', '0', '1', '2', '3', '4', '5', '6', '7', '8']):
        app.tapSound.play()
    if(key=='right'):
        setActiveScreen('main')
    elif(key=='0'):
        app.selectedCard=None
    elif(key=='1'):
        app.selectedCard=app.player.cardObjects[0]
    elif(key=='2'):
        app.selectedCard=app.player.cardObjects[1]
    elif(key=='3'):
        app.selectedCard=app.player.cardObjects[2]
    elif(key=='4'):
        app.selectedCard=app.player.cardObjects[3]
    elif(key=='5'):
        app.selectedCard=app.player.cardObjects[4]
    elif(key=='6'):
        app.selectedCard=app.player.cardObjects[5]
    elif(key=='7'):
        app.selectedCard=app.player.cardObjects[6]
    elif(key=='8'):
        app.selectedCard=app.player.cardObjects[7]

def cards_onMousePress(app, mouseX, mouseY):
    selected=shop_findButton(app, mouseX, mouseY)
    if(selected!=None):
        if(selected=='mainButton'):
            setActiveScreen('main')
        elif(selected=='shopButton'):
            setActiveScreen('shop')
    if(app.sfx and selected!=None):
        app.tapSound.play()

def cards_findButton(app, mouseX, mouseY):
    if(80<=mouseX<=135 and 740<=mouseY<795):
        return 'shopButton'
    elif(367.5<=mouseX<=402.5 and 740<=mouseY<=795):
        return 'mainButton'
    return None

def shop_onScreenActivate(app):
    pass

def shop_redrawAll(app):
    drawImage('assets/bg.png', 0, 0)
    drawLabel('How to Play:', 240, 75, size=48, font=app.font, fill='white', borderWidth=2, border='black')
    drawLabel('Navigation', 10, 150, size=24, font=app.font, fill='white', align='left')
    drawLabel('-Use the arrow keys or click to switch screens', 10, 180, size=12, font=app.font, fill='white', align='left')
    drawLabel('-Click on buttons and icons to press them', 10, 200, size=12, font=app.font, fill='white', align='left')
    drawLabel('Battle', 10, 240, size=24, font=app.font, fill='white', align='left')
    drawLabel('-Your deck is at the bottom of your hand', 10, 270, size=12, font=app.font, fill='white', align='left')
    drawLabel('-Your deck contains 8 cards, but only 4 are in your', 10, 290, size=12, font=app.font, fill='white', align='left')
    drawLabel('  hand at any given moment', 10, 310, size=12, font=app.font, fill='white', align='left')
    drawLabel('-Each card has an elixir cost, and you can only deploy', 10, 330, size=12, font=app.font, fill='white', align='left')
    drawLabel('  cards if you have enough elixir', 10, 350, size=12, font=app.font, fill='white', align='left')
    drawLabel('-Select a card using the number keys 1-4 or by clicking', 10, 370, size=12, font=app.font, fill='white', align='left')
    drawLabel('-Once selected, the red area represents deployable', 10, 390, size=12, font=app.font, fill='white', align='left')
    drawLabel('  squares; click the space to deploy the card', 10, 410, size=12, font=app.font, fill='white', align='left')
    drawLabel('-The objective of the game is to destroy the enemy', 10, 430, size=12, font=app.font, fill='white', align='left')
    drawLabel('  towers while defending your own', 10, 450, size=12, font=app.font, fill='white', align='left')
    drawLabel('-Double elixir occurs after 2 minutes, and triple elixir', 10, 470, size=12, font=app.font, fill='white', align='left')
    drawLabel('  starts after 3 minutes. After 6 minutes, the player', 10, 490, size=12, font=app.font, fill='white', align='left')
    drawLabel('  with more towers left standing wins. If the players', 10, 510, size=12, font=app.font, fill='white', align='left')
    drawLabel('  have the same # of towers, the game ends in a draw.', 10, 530, size=12, font=app.font, fill='white', align='left')
    drawImage('assets/logo.png', 50, 450, width=380, height=400)
    drawImage('assets/yawning_princess.png', 10, 530, width=120, height=120)
    drawImage('assets/laughing_king.png', 350, 630, width=150, height=110)
    #bottom bar
    drawRect(0, 740, 480, 60, fill=rgb(67, 81, 98))
    drawRect(0, 735, 480, 5, fill=rgb(111, 137, 167))
    #battle icon
    drawImage('assets/battle_icon.png', 212.5, 740, width=55, height=55)
    drawLabel('<Battle>', 240, 790, font=app.font, fill='white', size=17, bold=True)
    #cards icon
    drawImage('assets/card_icon.png', 80, 740, width=55, height=55)
    drawLabel('Cards>', 107.5, 790, font=app.font, fill='white', size=17, bold=True)
    #shop icon
    drawImage('assets/shop_icon.png', 347.5, 740, width=55, height=55)
    #glow to indicate which screen
    drawRect(300, 740, 180, 60, fill=rgb(114, 145, 176), opacity=30)
    drawLabel('<FAQ', 375, 790, font=app.font, fill='white', size=20, bold=True)

def shop_onKeyPress(app, key):
    if(app.sfx and key in ['left']):
        app.tapSound.play()
    if(key=='left'):
        setActiveScreen('main')

def shop_onMousePress(app, mouseX, mouseY):
    selected=shop_findButton(app, mouseX, mouseY)
    if(selected!=None):
        if(selected=='mainButton'):
            setActiveScreen('main')
        elif(selected=='cardButton'):
            setActiveScreen('cards')
    if(app.sfx and selected!=None):
        app.tapSound.play()

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
    #music
    if(app.music):
        app.battleMusic.play(loop=True, restart=True)

def battle_onStep(app):
    if(app.gameOver):
        if(app.music):
            app.battleMusic.pause()
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
    poppingIndices=[]
    for index, (unit, position) in enumerate(unitsList):
        if(not isinstance(unit, Spell) and unit.health<=0):
            poppingIndices.append(index)
            #unitsList.pop(index)
    for index in reversed(poppingIndices):
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
    drawImage('assets/arenabg.png', 0, 0, width=480, height=650)
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
        drawLabel('Elixir is full!', 240, 775, font=app.font, fill='red', size=24, bold=True, border='black')    
    drawLabel(math.floor(app.battle.p1.elixir), 30, 775, font=app.font, fill='white', size=24, bold=True)
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
    drawLabel(app.battle.p1.cardObjects[0].cost, 127.5, 742.5, font=app.font, fill='white', bold=True)
    drawLabel(app.battle.p1.cardObjects[1].cost, 212.5, 742.5, font=app.font, fill='white', bold=True)
    drawLabel(app.battle.p1.cardObjects[2].cost, 297.5, 742.5, font=app.font, fill='white', bold=True)
    drawLabel(app.battle.p1.cardObjects[3].cost, 382.5, 742.5, font=app.font, fill='white', bold=True)
    #drawing the next card
    drawRect(10, 705, 35, 45, fill=rgb(95, 66, 50))
    drawImage(app.battle.p1.cardObjects[4].image, 5, 705, width=35, height=45)
    drawLabel('Next:', 27.5, 695, fill='white', font=app.font, size=12, bold=True)
    #creating the board (Useful for debugging, not needed after board png overlayed)
    for row in range(app.rows):
            for col in range(app.cols):
                if((col, row)==app.friendlySelectedCell):
                    cellLeft, cellTop = getCellLeftTop(app, row, col)
                    cellWidth, cellHeight = getCellSize(app)
                    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill='white', opacity=50)
    #         else:
    #             drawCell(app, row, col)
    #drawing the depoyable squares over the board
    if(app.friendlySelectedCard!=None):
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                if(friendlyValidPosition(app, app.friendlySelectedCard, (col, row))):
                    cellleft, cellTop = getCellLeftTop(app, row, col)
                    cellWidth, cellHeight = getCellSize(app)
                    drawRect(cellleft, cellTop, cellWidth, cellHeight, fill='red', opacity=40)
    #drawing the rubble
    drawImage('assets/rubble.png', 53, 80, width=80, height=70)
    drawImage('assets/rubble.png', 347, 80, width=80, height=70)
    drawImage('assets/rubble.png', 187, 0, width=106, height=81)
    drawImage('assets/rubble.png', 53, 508, width=80, height=70)
    drawImage('assets/rubble.png', 347, 508, width=80, height=70)
    drawImage('assets/rubble.png', 187, 569, width=106, height=81)
    #drawing the towers over the rubble, once towers are destroyed rubble is visible
    ##drawing the red towers
    enemyLeft, enemyRight, enemyKing = checkTowers(app.enemyUnits)
    if(enemyLeft):
        drawImage('assets/red_princess_tower.png', 53, 80, width=80, height=70)
    if(enemyRight):
        drawImage('assets/red_princess_tower.png', 347, 80, width=80, height=70)
    if(enemyKing):
        drawImage('assets/red_king_tower.png', 187, 0, width=106, height=81)
    ##drawing the blue towers
    friendlyLeft, friendlyRight, friendlyKing = checkTowers(app.friendlyUnits)
    if(friendlyLeft):
        drawImage('assets/blue_princess_tower.png', 53, 508, width=80, height=70)
    if(friendlyRight):
        drawImage('assets/blue_princess_tower.png', 347, 508, width=80, height=70)
    if(friendlyKing):
        drawImage('assets/blue_king_tower.png', 187, 569, width=106, height=81)
    #drawing the units/buildings in friendlyUnits
    for friendlyUnit, friendlyPosition in app.friendlyUnits:
        if(isinstance(friendlyUnit, (Troop, Building, Tower))):
            drawUnit(app, friendlyUnit, friendlyPosition, 0)
    #repeating for enemy units
    for enemyUnit, enemyPosition in app.enemyUnits:
        if(isinstance(friendlyUnit, (Troop, Building, Tower))):
            drawUnit(app, enemyUnit, enemyPosition, 180) 
    #drawing timer
    drawTimer(app)  
    #drawing spell range if selected card is Spell
    drawSpellBorders(app)
    #game over overlay
    if(app.gameOver):
        drawRect(0, 0, 480, 800, fill='white', opacity=60)
        result=outcome(app.friendlyUnits, app.enemyUnits)
        if(result==True):
            app.winSound.play()
            endText='You Won!'
        elif(result==False):
            app.lossSound.play()
            endText='You Lost!'
        else:
            app.drawSound.play()
            endText='Draw!'
        drawLabel(endText, 240, 200, font=app.font, size=32, fill='white', border='black', borderWidth=2)
        drawRect(100, 500, 280, 120, fill=rgb(115, 147, 179), border=rgb(137, 207, 240), borderWidth=8)
        drawLabel('Continue', 240, 560, font=app.font, fill='white', size=24)
        drawLabel('(click or press any key)', 240, 590, font=app.font, fill='white', size=12)

def outcome(friendlyUnits, enemyUnits):
    #sometimes bugs if laggy: if king health is at -1 game lags and says draw
    #returns True if the player won, False if bot won, None is no one won
    friendlyLeft, friendlyRight, friendlyKing = checkTowers(friendlyUnits)
    enemyLeft, enemyRight, enemyKing = checkTowers(enemyUnits)
    if(friendlyKing==None):
        return False
    if(enemyKing==None):
        return True
    friendlyCrowns=0
    enemyCrowns=0
    for fstatus in (friendlyLeft, friendlyRight):
        if fstatus==True:
            friendlyCrowns+=1
    for estatus in (enemyLeft, enemyRight):
        if estatus==True:
            enemyCrowns+=1
    if(friendlyCrowns==enemyCrowns):
        return None
    else:
        return friendlyCrowns>enemyCrowns

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

def drawUnit(app, unit, position, rotationAngle):
    col, row = position
    adjustedX, adjustedY = cellToPixel(app, row, col)
    if(isinstance(unit, (Troop, Building))):
        drawImage(unit.sprite, adjustedX, adjustedY, align='center', rotateAngle=rotationAngle)
    drawLabel(rounded(unit.health), adjustedX, adjustedY, size=14, font=app.font, fill='white')

def rounded(n):
    return math.floor(n+0.5) if n>0 else math.floor(n-0.5)

def drawTimer(app):
    seconds = math.floor(app.remainingTime)
    minutes = seconds//60
    seconds -= minutes*60
    secondsString=f'0{seconds}' if(seconds<10) else str(seconds)
    minutesString=f'0{minutes}' if(minutes<10) else str(minutes)
    time = f'{minutesString}:{secondsString}'
    drawLabel(time, 440, 20, fill='white', font=app.font, size=18, bold=True, border='black', borderWidth=2)

def drawCell(app, row, col):
    #make opacity 100 for debug
    colorList=['green', 'blue', 'brown', 'black', 'red']
    colorIndex=app.board[row][col]
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=colorList[colorIndex], border='black', borderWidth=app.cellBorderWidth, opacity=0)
    
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
    if(app.gameOver):
        app.tapSound.play()
        setActiveScreen('main')
        if(app.music):
            app.battleMusic.pause()
        app.menuMusic.play()
    else:
        if(app.sfx and key in ['1', '2', '3', '4', 'escape']):
            app.tapSound.play()
        if(key=='escape'):
            if(app.music):
                app.battleMusic.pause()
                app.menuMusic.play()
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
    if(not app.gameOver):
        app.friendlySelectedCell=battle_getCell(app, mouseX, mouseY)

def battle_onMousePress(app, mouseX, mouseY):
    if(app.gameOver):
        if(100<=mouseX<=380 and 500<=mouseY<=620):
            if(app.sfx):
                app.tapSound.play()
            if(app.music):
                app.battleMusic.pause()
                app.menuMusic.play()
            setActiveScreen('main')
    else:
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
            elif(left==None and right==None):
                return selectedRow>7
            elif(left==None):
                return selectedRow>7 and selectedCol<9
            elif(right==None):
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
            elif(left==None and right==None):
                return selectedRow<24
            elif(left==None):
                return selectedRow<24 and selectedCol<9
            elif(right==None):
                return selectedRow<24 and selectedCol>=9

def enemyPlaceCard(app):
    #currently only deploys archers at constant time intervals
    app.enemySelectedCard=app.battle.p2.cardObjects[0]
    #app.battle.p2.deployCard(app, app.enemySelectedCard, (8, 8), 0, app.enemyUnits, app.enemySelectedCard)
    averageCol, averageRow = getWeights(app.friendlyUnits)
    if(averageCol<8.5):
        newCol=random.randint(0, 8)
    else:
        newCol=random.randint(9, 17)
    newRow=max(0, math.floor(averageRow)-6)
    if(enemyValidPosition(app, app.enemySelectedCard, (newCol, newRow))):
        app.battle.p2.deployCard(app, app.enemySelectedCard, (newCol, newRow), 0, app.enemyUnits, app.enemySelectedCard)
    else:
        pass

def getWeights(unitsList):
    colTotal, rowTotal = 0, 0
    total=0
    for troop, position in unitsList:
        if(not isinstance(troop, Tower)):
            total+=1
            col, row = position
            colTotal+=col
            rowTotal+=row
    if(total== 0):
        return (0, 0)
    return colTotal/total, rowTotal/total

#returns the format as (x, y) or (col, row)
def battle_getCell(app, mouseX, mouseY):
    if(mouseX>480 or mouseY>650):
        return None
    else:
        cellWidth=app.boardWidth/app.cols
        cellHeight=app.boardHeight/app.rows
        return math.floor(mouseX/cellWidth), math.floor(mouseY/cellHeight)

def settings_onScreenActivate(app):
    app.changingName=False
    app.newName=''
    app.nameTooShort=False
    
def settings_redrawAll(app):
    #Music and sfx icons are from https://iconduck.com/icons/269893/speaker and https://www.flaticon.com/free-icon/sound-effect_2217608
    #username icon from https://www.vecteezy.com/png/19879186-user-icon-on-transparent-background
    #overview
    drawImage('assets/bg.png', 0, 0)
    drawLabel('Settings', 240, 40, font=app.font, fill='white', size=48, bold=True, border='black')
    drawLabel('(press escape to return)', 240, 80, font=app.font, fill='white', size=12)
    #music
    if(app.music):
        musicLabel='Enabled'
        musicFill='lime'
        musicBorder='green'
    else:
        musicLabel='Disabled'
        musicFill=rgb(210, 43, 43)
        musicBorder=rgb(238, 75, 43)
    drawImage('assets/speaker.png', 10, 120, width=50, height=50)
    drawLabel('Music:', 10, 190, font=app.font, fill='white', size=16, align='left')
    drawRect(100, 120, 300, 80, fill=musicFill, border=musicBorder, borderWidth=8)
    drawLabel(musicLabel, 250, 160, font=app.font, fill='white', size=24)
    if(app.sfx):
        sfxLabel='Enabled'
        sfxFill='lime'
        sfxBorder='green'
    else:
        sfxLabel='Disabled'
        sfxFill=rgb(210, 43, 43)
        sfxBorder=rgb(238, 75, 43)
    #sfx
    drawImage('assets/sfx.png', 10, 250, width=50, height=50)
    drawLabel('SFX:', 10, 320, font=app.font, fill='white', size=16, align='left')
    drawRect(100, 250, 300, 80, fill=sfxFill, border=sfxBorder, borderWidth=8)
    drawLabel(sfxLabel, 250, 290, font=app.font, fill='white', size=24)
    #username
    drawImage('assets/username.png', 10, 380, width=50, height=50)
    drawLabel('User:', 10, 450, font=app.font, fill='white', size=16, align='left')
    drawRect(100, 380, 300, 80, fill=rgb(115, 147, 179), border=rgb(137, 207, 240), borderWidth=8)
    if(app.changingName):
        drawLabel(app.newName, 250, 420, font=app.font, fill='white', size=24)
        drawLabel('Press enter to save!', 250, 440, font=app.font, fill='white', size=12)
    else:
        drawLabel(app.username, 250, 420, font=app.font, fill='white', size=24)
    if(app.nameTooShort):
        drawLabel('Username must be at least of length 3!', 250, 470, font=app.font, fill='red', size=12)

def settings_onKeyPress(app, key):
    if(app.sfx and key in ['escape', 'enter']):
        app.tapSound.play()
    app.nameTooShort=False
    if(key=='escape'):
        setActiveScreen('main')
    if(app.changingName):
        if((key in string.ascii_letters or key in string.digits) and len(app.newName)<=10):
            app.newName+=key
        elif(key=='backspace'):
            app.newName=app.newName[:-1]
        elif(key=='enter'):
            if(len(app.newName)<3):
                app.nameTooShort=True
            else:
                app.changingName=False
                app.username=app.newName
                app.newName=''

def settings_onMousePress(app, mouseX, mouseY):
    if(100<=mouseX<=400 and 120<=mouseY<=200):
        app.music = not app.music
        if(app.sfx):
            app.tapSound.play()
        if(not app.music):
            app.menuMusic.pause()
        else:
            app.menuMusic.play()
    elif(100<=mouseX<=400 and 250<=mouseY<=330):
        if(app.sfx):
            app.tapSound.play()
        app.sfx = not app.sfx
    elif(100<=mouseX<=400 and 380<=mouseY<=460):
        if(app.sfx):
            app.tapSound.play()
        app.changingName=True

def main():
    runAppWithScreens(initialScreen='main');

main()
