#A SUPER CLASS FOR ALL OBJECTS THAT LIVE IN PLAY

#ABSTRACT
class Permanent():

    _hidden = True
    typeName = None #ABSTRACT STATIC STRING

    def __init__(self, card, costSpent):
        self._card = card
        self._spent = costSpent
        self._scrolls = 0
        self._purses = 0

    #TODO: clean up these if-statements
    def getDispText(self, forceShow = False):
        text = ""
        if self._hidden and not forceShow:
            text = "Hidden "+sel.typeName+", "+str(self._spent)+"G"
            if self._scrolls > 0:
                text += ", " + str(self._scrolls) + " Scrolls"
            if self._purses> 0:
                text += ", " + str(self._purses) + " Purses"
        else: 
            text = self.card.getDispText()
        if self._hidden:
            text = "~"+text+"~"
        return text