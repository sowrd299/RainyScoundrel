from permanents import Permanent 
import actions

spyName = "Spy"
thieveName = "Thieve"
attackName = "Attack"

class Agent(Permanent):

    typeName = "Agent"
    scrollsName = "Scrolls"

    def __init__(self, card, costSpent):
        super().__init__(card, costSpent)
        self._exh = True #GAME LOGIC: spawn exhausted
        self._dead = False

    #GETTERS AND SETTERS
    def isExhausted(self):
        return self._exh

    def exhaust(self):
        self._exh = True

    def unexhaust(self):
        self._exh = False

    def reveal(self):
        self._hidden = False

    def getSpyVal(self):
        return self._card._spyVal

    def getThiefVal(self):
        return self._card._thiefVal

    #Returns the general combat stat
    def getCombatVal(self):
        return self._card._thiefVal

    """ #Removed:
    def canSpy(self):
        return not self.getExhausted()

    def canThieve(self):
        return not self.getExhausted()

    def canAttack(self):
        return not self.getExhausted()
    """

    def getActions(self, gold = 100):
        if not self.isExhausted():
            return [ self.ThieveAction(self) ] #TODO: CREATE SPY, THIEF AND COMBAT ACTIONS
        return []

    def die(self, cause : str):
        self._dead = True

    def isDead(self):
        return self._dead

    #IO

    def getDispText(self, private):
        text = super().getDispText(private)
        if self._exh:
            text = "["+text+"]"
        return text

    #GAMEPLAY FUNCIONS

    def turn(self):
        self.unexhaust()

    def _act(self, counter):
        self.exhaust()
        self._counters[counter] += 1

    def spy(self):
        self._act(self.scrollsName)
        return self.getSpyVal()

    def thieve(self):
        self._act(self.pursesName)
        return self.getThiefVal()

    #COMBAT
    #note: attack devided up to allow as much 
    #       flexibility with special abilities as possible

    #the main attack function; runs all of combat.
    #returns list of units killed
    def attack(self, other):
        #CS
        cs = self._getCombatScore(other)
        osc = other._getCombatScore(self)
        #Deathlist
        deathList = []
        deathList = self._getKilled(other, cs, ocs, deathList)
        deathList = other._getKilled(self, ocs, cs, deathList)
        #Postcombat
        self._postCombat(other, deathList)
        other._postCombat(self, deathList)
        #Return
        return deathList

    #returns score to be used in a specific combat
    def _getCombatScore(self, other):
        return self.getCombatVal()

    #appends people who will be killed to the deathList
    def _getKilled(self, other, cs, othercs, deathList):
        if cs <= ocs:
            desthList.append(self)
        return deathList

    #ability operturnity only
    def _postCombat(self, other, deathList):
        pass

    #INNER CLASSES

    #the thief action
    class ThieveAction(actions.Action):
        def __init__(self, thief):
            super().__init__(thieveName, thief.thieve, [], False, "gold")