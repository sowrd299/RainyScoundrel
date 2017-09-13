import actions
from pieces import Piece

#A file containing card-related abstract classes

#ABSTRACT
class Card(Piece):
    def __init__(self, name, cost):
        self._name = name
        self._cost = cost

    #GETTERS AND SETTERS
    def getName(self):
        return self._name
    def getCost(self):
        return self._cost

    
    #IO
    #Text to display the card in-game
    def getDispText(self, private = False):
        return "("+str(self._cost)+"G) "+self._name

    #GAMEPLAY

    def getActions(self, gold = 100): 
        r = []
        if self.canPlay(gold):
            r.append(self.PlayAction(self, gold))
        return r

    #returns true if can play with the specified paramers.
    #assumes unspecified paraters are sufficient
    def canPlay(self, gold = 100):
        return gold >= self.getCost()

    #abstract
    #returns amount spent (for purposes of the Play action)
    def play(self, spent):
        raise NotImplementedError

    #INNER CLASSES
    class PlayAction(actions.Action):
        
        def __init__(self, card, gold):
            self._card = card
            pred = lambda x : self._card.canPlay(x) and x <= gold
            dispText = "How much do you want to spend (cost is "+str(self._card._cost)+"G, "+str(gold)+"G available)"
            self._spend_arg = actions.ActionArg("Spend",int,pred,dispText = dispText)
            super().__init__("Play", card.play, [self._spend_arg], False, "ERROR IF THIS OUTCOME TYPE USED")

        def go(self):
            super().go()
            return actions.ActionOutcome(public = True, gold = -1*self._spend_arg.getVal(), discardList = [self._card])

#ABSTRACT
class PermCard(Card):
    
    spawnClass = None #The class of object the card spawns

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def play(self, targetArea, costPayed):
        targetArea.append(self.spawnClass(self, costPayed))

    class PlayAction(Card.PlayAction):

        def __init__(self, card : Card, gold):
            super().__init__(card, gold)
            self._outcomeType = "spawnList"

        def go(self):
            #create and insert the spawn list
            argSpawnList = actions.ActionArg("SPAWN LIST", list)
            spawnList = []
            argSpawnList.setVal(spawnList)
            self._args.insert(0, argSpawnList)
            #spawn the permanent:
            oc = super().go()
            #add the spawn list to the outcome, and return it
            oc.spawnList = spawnList
            return oc