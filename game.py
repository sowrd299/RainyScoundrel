from players import Player 

#A CLASS TO REPRESENT ONE GAME

class Game():

    #GAME CONSTANTS
    startingGold = 4
    startingHand = 4
    cluesToWin = 20

    def __init__(self, decks):
        count = iter(range(100))
        self._players = [ Player("Player "+str(next(count)), self.startingGold, self.startingHand, deck) for deck in decks ]
        self._turn = 0

    #GETTERS AND SETTERS

    def getActivePlayer(self):
        return self._players[self._turn]

    #IO

    def getDispText(self, displayArgs = {}):
        text = ""
        ap = self.getActivePlayer()
        for p in self._players:
             if not p is ap:
                 text += p.getDispText(False,  **(displayArgs[p] if p in displayArgs.keys() else dict())) +"\n"
        text += ap.getDispText(True, **(displayArgs[ap] if ap in displayArgs.keys() else dict()))        
        return text

    #GAME LOGIC

    def turn(self):
        self._turn = (self._turn + 1) % len(self._players)
        self.getActivePlayer().turn()