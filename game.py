from players import Player 
from absCards import Card
from pieces import Piece
import actions

#A CLASS TO REPRESENT ONE GAME

class Game():

    #action constants
    actionEndTurn = "END TURN"

    #GAME CONSTANTS
    _startingGold = 4
    _startingHand = 4
    _cluesToWin = 20

    def __init__(self, decks, playerControllerClasses):
        count = iter(range(100))
        self._players = [ Player("Player "+str(next(count)), self._startingGold, self._startingHand, deck) for deck in decks ]
        self._playerControllers = [ pcc(self) for pcc in playerControllerClasses ]
        self._turn = 0

    #GETTERS AND SETTERS

    def _getActivePlayer(self):
        return self._players[self._turn]

    def _getActivePlayerController(self):
        return self._playerControllers[self._turn]

    def getCardsThat(self, pred, players = []):
        if players == []:
            players = [self._getActivePlayer()]
        return [card for player in players for card in player.getAllActiveCards() if pred(card)]

    #IO

    def getDispText(self, displayArgs, player = None):
        text = ""
        if player == None:
            player = self._getActivePlayer()
        for p in self._players:
             if not p is player:
                 text += p.getDispText(False,  **(displayArgs)) + "\n"
        text += player.getDispText(True, **(displayArgs))
        return text

    #GAME LOGIC

    #ONCE THROUGH THE MAIN GAME LOOP
    #returns wether or not the game is still in progress
    def main(self):
        #basic variables
        choice = None
        apc = self._getActivePlayerController()
        ap = self._getActivePlayer()
        #select an action 
        while choice == None:
            _actions = { id(choice) : choice.getActions(ap._gold.priv()) for choice in ap.getAllActiveCards() } #TODO: STOP VIOLATING PRIVACY HERE
            choice = apc.chooseFromCards(self.getCardsThat( lambda x : len(_actions[id(x)]) > 0 ))
        #handle choice selections
        if isinstance(choice , Piece):
            action = apc.chooseFromList(_actions[id(choice)])
            self._act(action, ap, apc)
            #TODO: report result of act to players
        #handle command strings
        else:
            if choice == self.actionEndTurn:
                self._next_turn()
        #TODO: insert end of game code here
        return True
        
    #CARRY OUT AN ACTION
    def _act(self, action, player = None, pc = None):
        #DEFAULT TO ACTIVE PLAYER AND CONTROLLER
        if player == None:
            player = self._getActivePlayer()
        if pc == None:
            pc = self._getActivePlayerController()
        #ARGS
        for arg in action.getArgs():
            if arg.getFriendly():
                pc.chooseArg(arg)
            else:
                for p in self._playerControllers():
                    if not p is pc:
                        p.chooseArg
        #RESOLVE THE ACTION
        oc = action.go()
        deathList = oc.deathList
        player.processOutcome(oc)
        for p in self._players:
            p.processOutcome(actions.ActionOutcome(True, deathList = deathList))

    def _next_turn(self):
        self._turn = (self._turn + 1) % len(self._players)
        ap = self._getActivePlayer()
        ap.turn()
        ap.gen()