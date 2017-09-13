from collections import defaultdict
from pieces import Piece

#A SUPER CLASS FOR ALL OBJECTS THAT LIVE IN PLAY
#TODO: organize this file

#ABSTRACT
class Permanent(Piece):

    _hidden = True
    typeName = None #ABSTRACT STATIC STRING
    pursesName = "Purses"

    def __init__(self, card, costSpent):
        self._card = card
        self._spent = costSpent
        self._counters = defaultdict(int)

    def getName(self):
        return self._card._name
    def getCost(self):
        return self._card._cost

    #TODO: clean up these if-statements
    def getDispText(self, forceShow = False):
        text = ""
        if self._hidden and not forceShow:
            text = "Hidden "+self.typeName+", "+str(self._spent)+"G"
            for counter, count in self._counters.items():
                text += ", " + str(count) + " " + counter
        else: 
            text = self._card.getDispText(True)
        if self._hidden:
            text = "~"+text+"~"
        return text

    def isDead(self):
        raise NotImplementedError

    def getActions(self):
        raise NotImplementedError

    def turn(self):
        pass