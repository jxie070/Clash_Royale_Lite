from cmu_graphics import *
from entity import Card
class Player:
    def __init__(self, name, cards):
        self.elixir=None
        self.name=name
        self.cards=cards
        self.cardObjects=None

    def __repr__(self):
        return f'Player(name={self.name}, cards={self.cards})'

    #enemy/friendly selected list, enemy/friendly selectedCard
    def deployCard(self, app, card, selectedCell, selectedIndex, selectedList, selectedCard):
        if self.elixir>=card.cost:
            self.elixir-=card.cost
            
            selectedList.append((selectedCard.clone(), selectedCell))
            self.cards.append(self.cards.pop(selectedIndex))
            self.cardObjects=[Card.cardLibrary[card] for card in self.cards]
            #resetting the selected cards
            app.card1bg=rgb(95, 66, 50)
            app.card2bg=rgb(95, 66, 50)
            app.card3bg=rgb(95, 66, 50)
            app.card4bg=rgb(95, 66, 50)
            #print(app.battle.p1.cards)
        #else:
            #print('Not enough elixir!')


    