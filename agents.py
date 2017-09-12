from permanents import Permanent 

class Agent(Permanent):

    typeName = "Agent"

    def __init__(self, card, costSpent):
        super().__init__(card, costSpent)
        self._exh = False
        self._dead = False

    #GETTERS AND SETTERS
    def getExhausted(self):
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

    def canSpy(self):
        return not self.getExhausted()

    def canThieve(self):
        return not self.getExhausted()

    def canAttack(self):
        return not self.getExhausted()

    def die(self, cause):
        self._dead = True

    def isDead(self):
        return self._dead

    #IO

    def getDisplayText(self):
        text = Permanent.getDisplayText(self)
        if self._exh:
            text = "["+text+"]"
        return text

    #GAMEPLAY FUNCIONS

    def turn(self):
        self.unexhaust()

    def _act(self, counter):
        self.exhaust()
        exec("self."+counter+"+=1")

    def spy(self):
        self._act("_scrolls")
        return self.getSpyVal()

    def thieve(self):
        self._act("_purses")
        return self.getThiefVal()

    #COMBAT
    #note: attack devided into three methods to allow as much 
    #flexibility with special abilities as possible

    def attack(self, other):
        osc = other._combat(self.getCombatScore(other))
        self._combat(other,osc)

    #Returns the specific value to be used in combat
    def getCombatScore(self,other):
        return self.getCombatVal()

    #helper function for carrying out combat
    #returns Combat Score
    def _defend(self, other, othercs):
        cs = self.getCombatScore(other)
        if scs <= ocs:
            self.die("combat")
        return cs 