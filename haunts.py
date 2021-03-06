from permanents import Permanent

preventName = "Prevent"

class Haunt(Permanent):

    typeName = "Haunt"
    marksName = "Marks"

    def __init__(self, card, costSpent):
        super().__init__(card, costSpent)
        self._shroud = card._shroudVal

    #GETTERS AND SETTERS

    def getShroud(self):
        return self._shroud

    def getGenVal(self):
        return self._card._genVal

    def die(self):
        self._shroud = 0

    def isDead(self):
        return self._shroud <= 0 #GAME LOGIC

    #IO

    def getDispText(self, private):
        text = super().getDispText(private).split(' ')
        if private:
            text[-1] = str(self.getShroud()) + "/" + text[-1]
        return ' '.join(text)

    #GAME LOGIC

    def gen(self):
        self._counters[self.pursesName] += 1
        return self.getGenVal()

    #To be called whenever the Haunt prevents an action
    def prevent(self, action):
        self.damage(1, preventName)
        
    #Deals "damage" to the haunt
    def damage(self, damage, cause : str, public : bool = True):
        self._shroud -= damage
        if public:
            self._counters[self.marksName] += damage