import random
from absCards import Card 

class Deck():

    def __init__(self, cards = None):

        self._cards = None
        #SWITCH BASED ON FORMAT CARDS PRIVED IN
        if cards.__iter__ and isinstance(next(iter(cards)), Card):
            self._cards = list(cards)

    def shuffle(self):
        old_cards = list(self._cards) 
        new_cards = []
        while len(old_cards) > 0:
            c = old_cards[random.randrange(len(old_cards))]
            old_cards.remove(c)
            new_cards.append(c)
        self._cards = new_cards

    def draw(self, n):
        return [ self._draw() for i in range(n) ]

    def _draw(self):
        return self._cards.pop()