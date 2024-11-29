from cmu_graphics import *
from cards import Card
class Player:
    def __init__(self, name, cards):
        self.elixir=None
        self.name=name
        self.cards=cards
        self.cardObjects=None

    def __repr__(self):
        return f'Player(name={self.name}, cards={self.cards})'

    def deployCard(self, app, card, selectedCell, selectedIndex):
        if self.elixir>=card.cost:
            self.elixir-=card.cost
            app.friendlyUnits.append((app.selectedCard.clone(), selectedCell))
            app.selectedCard=None
            app.battle.p1.cards.append(app.battle.p1.cards.pop(selectedIndex))
            app.battle.p1.cardObjects=[Card.cardLibrary[card] for card in app.battle.p1.cards]
            #resetting the selected cards
            app.card1bg=rgb(95, 66, 50)
            app.card2bg=rgb(95, 66, 50)
            app.card3bg=rgb(95, 66, 50)
            app.card4bg=rgb(95, 66, 50)
            print(app.battle.p1.cards)
        else:
            print('Not enough elixir!')


    