#A file containing card-related abstract classes

#ABSTRACT
class Card():
    def __init__(self, name, cost):
        self._name = name
        self._cost = cost

    #GETTERS AND SETTERS
    def getCost(self):
        return self._cost

    #RELATIONALS
    def __eq__(self, other):
        return self._name == other._name

    def __lt__(self, other):
        return self._cost < other._cost or (self._cost == other._cost and self._name < other._name)
    
    #IO
    #Text to display the card in-game
    def getDispText(self, private = False):
        return "("+str(self._cost)+"G) "+self._name


#ABSTRACT
class PermCard(Card):
    
    spawnClass = None #The class of object the card spawns

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def play(self, target, costPayed):
        target.add(self.spawnClass(self, costPayed))
    