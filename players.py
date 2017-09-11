from agents import Agent 
from haunts import Haunt 
from absCards import Card 
from collections import defaultdict

class Player():

    def __init__(self, name, start_gold, start_hand, deck):
        self._name = name
        self._gold = self.pubPrivRes(start_gold) #primary resources
        self._clues = self.pubPrivRes(0) #victory points
        self._hand = list(deck.draw(start_hand)) #cards in hand
        self._pub_hand = list()
        self._play = list() #agents in play
        self._deck = deck

    #GETTERS AND SETTERS

    def getName(self):
        return self._name

    def getAgents(self):
        return self._get_perms_of_class(Agent)

    def getHaunts(self):
        return self._get_perms_of_class(Haunt)

    def _get_perms_of_class(self, c):
        return [p for p in self._play if isinstance(p,c)]

    #IO

    def getDispText(self, private : bool, agentsList = None, hauntsList = None, handList = None):

        def listCards(cards, cols = 2):
            text = ""
            num = 0
            l = len(cards) - 1 #last index
            for key,card in ( ( (None,e) if isinstance(e,Card) else (e,cards[e]) ) for e in sorted(cards)):
                text += "\t" 
                if key:
                    text += str(key) + ": "
                text += card.getDispText(private)
                num += 1
                if num % cols == 0 and num  < l:
                    #newline after every N cols, but never at the end of the list
                    text += "\n"
            return text

        #HEADER
        text = "~~"+self._name + "~ " +self._gold.getDispText("G", private) + " ~ " + self._clues.getDispText("Clues", private)+" ~~\n"
        #CARDS
        text += "AGENTS:\n"
        text += listCards(agentsList or self.getAgents())
        text += "\nHAUNTS:\n"
        text += listCards(hauntsList or self.getHaunts())
        if private:
            text += "\nHAND:\n"
            text += listCards(self._hand)
        return text

    #GAME LOGIC

    def draw(n):
        self._hand.union(self._deck.draw(n))

    def turn(self):
        for p in self._play:
            if p.turn:
                p.turn()

    def canPlay(self, card):
        return card.getCost() <= self._gold.priv()

    #TODO: assumes all cards are permanent cards! Stop that!
    def play(self, card, costPaid):
        card.play(self._play,costPaid)
        self.gold.add(-1*costPaid,True) 

    #INNER CLASSES
    class pubPrivRes():

        def __init__(self, startVal, pubStartVal = None):
            self._priv = startVal
            self._pub = pubStartVal if pubStartVal != None else startVal
            self._tracked_priv = defaultdict(int)

        def pub(self):
            return self._pub

        def priv(self):
            return self._priv

        #add an amount to the value
        #pub :: bool; whether or not the changes should be public
        #source :: Object; the source to attribute the changes to
        def add(self, val, pub, source = None):
            self._priv += val
            self._pub += val * int(pub)
            if not pub and source != None:
                self._tracked_priv[source] += val

        #make all tracked private changes from a source public
        def reveal(self, source):
            self._pub += self._tracked_priv[source]
            del self._tracked_priv[source]

        def getDispText(self, accronym, private):
            return (str(self.priv()) if private else "?") + accronym +" ("+str(self.pub())+ accronym + " Public)"