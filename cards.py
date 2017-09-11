#A file containing card-related non-abstract classes

from agents import Agent
from haunts import Haunt
from absCards import PermCard

class AgentCard(PermCard):

    spawnClass = Agent

    def __init__(self, name, cost, spyVal, combatVal, thiefVal):
        super().__init__(name, cost)
        self._spyVal = spyVal
        self._combatVal = combatVal
        self._thiefVal = thiefVal

    def getDispText(self, private):
        text = PermCard.getDispText(self)+" "
        text += str(self._spyVal) + "Sp|"
        text += str(self._combatVal) + "Cm|"
        text += str(self._thiefVal) + "Th"
        return text


class HauntCard(PermCard):

    spawnClass = Haunt

    def __init__(self, name, cost, shroudVal, genVal):
        super().__init__(name, cost)
        self._shroudVal = shroudVal
        self._genVal = genVal

    def getDispText(self, private):
        text = PermCard.getDispText(self)+" "
        text += str(self._shroudVal) + "Sh|"
        text += str(self._genVal) + "Gp"