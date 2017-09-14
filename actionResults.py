from pieces import Piece
from players import Player

#ABSTRACT
#a class to represent effects card actions can have of the broader game state
class ActionResult():

    def __init__(self, source : Piece, public : bool, val : object):
        self._source = source #the game piece responsible for the effect
        self._val = val #the other argument necessary
        self._public = public

    #returns completion status
    #   true => finished reolving
    #   false => not complete (may need to be applied to other players)
    def resolve(self, player : Player):
        raise NotImplementedError

#ABSTRACT
#a class to give the player a certain resource
class ResourceResult(ActionResult):

    def __init__(self, source, val : int, public, resource : str):
        super().__init__(source, public, val)
        self._resource = resource #what resource to gain

    def resolve(self, player):
        player.gainResource(self._resource, self._val, self._source, self._public)
        return True

class GoldResult(ResourceResult):
    def __init__(self, source, public, val):
        super().__init__(source, public, val, Player.goldAcc)

class CluesResult(ResourceResult):
    def __init__(self, source, public, val):
        super().__init__(self, source, val, public, Player.cluesAcc)

#ABSTRACT
#for results that involve apply some affect to one or more pieces
class PieceListResult(ActionResult):
    def __init__(self, source, public, val : [Piece]):
        super().__init__(source, public, val)

    def resolve(self, player : Player):
        ac = player.getAllActiveCards()
        for piece in self._val:
            if piece in ac:
                self._resolve(piece, player)
                self._val.remove(piece)
        return len(self._val) == 0

    def _resolve(self, piece, player):
        raise NotImplementedError

#TODO: MAKE THE COMBINATION OF THIS WITH PieceListResult slightly less inefficient
#NOTE: CURRENTLY ONLY SUPPORTS AGENTS
class DeathListResult(PieceListResult):
    def _resolve(self, piece, player):
        #TODO: ADD THIS METHOD TO PLAYER
        player.kill(piece)

class SpawnListResult(PieceListResult):
    def _resolve(self, piece, player):
        #TODO: you know the drill
        player.spawn(piece)

class DiscardListResult(PieceListResult):
    def _resolve(self, piece, player):
        #TODO: yup, add it to player
        player.discard(piece)

class RevealListResult(PieceListResult):
    def _resolve(self, piece, player):
        player.reveal(piece)

class DrawResult(PieceListResult):
    def resolve(self, player):
        player.draw(self._val)
        return True

#TODO: add a "publicies" effect, that adds cards to the pub-hand