import actions
import absCards

class PlayerControllerNotSuportedError(Exception):
    pass

#ABSTRACT
#primaray source of input (and, at the moment, output)
#TODO: Make serporate output class
class PlayerController():

    def __init__(self, game):
        self._game = game

    def chooseFromCards(self, choices):
        raise NotImplementedError

    def chooseFromList(self, choices):
        raise NotImplementedError

    def chooseArg(self, arg : actions.ActionArg):
        if arg.getType() == int:
            return self.chooseNumber(arg.getDispText(), arg.setVal)
        raise PlayerControllerNotSuportedError("Cannot handle Action Argument of type: "+str(arg.getType()))

    def chooseNumber(self, prompt, pred):
        raise NotImplementedError