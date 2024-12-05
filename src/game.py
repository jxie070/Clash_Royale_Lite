import random
from player import Player

class Game:
    def __init__(self, p1Name, p2Name, p1Deck, p2Deck):
        self.p1=Player(p1Name, p1Deck)
        self.p2=Player(p2Name, p2Deck)
    #debug functions
    def printNames(self):
        print(self.p1.name, self.p2.name)

    def printDecks(self):
        print(f'Player1 Deck: {self.p1.cards}, Player2 Deck: {self.p2.cards}')

    def createBoard(self):
        #18 cols, 32 rows
        #0 = deployable spaces
        board=[[0]*18 for row in range(32)]
        #1 = river lane
        board[15]=[1]*18
        board[16]=[1]*18
        #2 = bridge tiles
        board[15][3]=2
        board[16][3]=2
        board[15][14]=2
        board[16][14]=2
        #3 = princess tower tiles
            #red
        self.setSquare(board, 4, 7, 2, 5, 3)
        self.setSquare(board, 4, 7, 13, 16, 3)
            #blue
        self.setSquare(board, 25, 28, 2, 5, 3)
        self.setSquare(board, 25, 28, 13, 16, 3)
        #4 = king tower tiles
            #red
        self.setSquare(board, 0, 4, 7, 11, 4)
            #blue
        self.setSquare(board, 28, 32, 7, 11, 4)
        return board
    
    def setSquare(self, board, sRow, eRow, sCol, eCol, n):
        for row in range(sRow, eRow):
            for col in range(sCol, eCol):
                board[row][col]=n

    def shuffleStartingHands(self):
        #takes the cards from both players, finds 4 starting hand cards and moves them to the front of card list
        p1StartingHand=random.sample(self.p1.cards, 4)
        for card in p1StartingHand:
            self.p1.cards.insert(0, self.p1.cards.pop(self.p1.cards.index(card)))
        p2StartingHand=random.sample(self.p2.cards, 4)
        for card in p2StartingHand:
            self.p2.cards.insert(0, self.p2.cards.pop(self.p2.cards.index(card)))

    
