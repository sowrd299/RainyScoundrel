from permanents import Permanent

class Haunt(Permanent):

    typeName = "Haunt"

    def __init__(self, card, costSpent):
        super().__init__(card, costSpent)