#ABSTRACT 
#the common ancestor of all game pieces
class Piece():

    #GETTERS AND SETTERS
    
    def getCost(self):
        raise NotImplementedError

    def getName(self):
        raise NotImplementedError

    def getDispText(self):
        raise NotImplementedError

    #RELATIONALS

    def __eq__(self, other):
        return isinstance(other, Piece) and self.getName() == other.getName()

    def __lt__(self, other):
        return self.getCost() < other.getCost() or (self.getCost() == other.getCost() and self.getName() < other.getName())

    #GAME LOGIC
    
    def getActions(self, gold = 100):
        raise NotImplementedError