from permanents import Permanent 

class Agent(Permanent):

    typeName = "Agent"

    def __init__(self, card, costSpent):
        super().__init__(card, costSpent)
        self._exh = False
        self._hidden = True

    #GETTERS AND SETTERS

    def exhaust(self):
        self._exh = True

    def unexhaust(self):
        self._exh = False

    def reveal(self):
        self._hidden = False

    #IO

    def getDisplayText(self):
        text = Permanent.getDisplayText(self)
        if self._exh:
            text = "["+text+"]"
        return text

    #GAMEPLAY FUNCIONS

    def turn(self):
        self.unexhaust()