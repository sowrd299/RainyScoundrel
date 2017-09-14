import agents #cannot import agent: causes import loop
from haunts import Haunt 
from absCards import Card 
from collections import defaultdict
from actions import ActionOutcome

class Player():

    #RESOURCE ACCRONYMS
    goldAcc = "G"
    cluesAcc = " Clues"

    #NOTE: Most begining of game setup done here
    def __init__(self, name, start_gold, start_hand, deck):
        self._name = name
        self._gold = self.pubPrivRes(start_gold) #primary resources
        self._clues = self.pubPrivRes(0) #victory points
        self._pub_hand = list() #TODO: Implement card reveal/public hands
        self._play = list() #agents in play
        self._deck = deck
        deck.shuffle()
        self._hand = list(deck.draw(start_hand)) #cards in hand

    #GETTERS AND SETTERS

    def getName(self):
        return self._name

    #returns all cards that can be interacted with
    def getAllActiveCards(self):
        return self._play + self._hand

    def getAgents(self):
        return self._get_perms_of_class(agents.Agent)

    def getHaunts(self):
        return self._get_perms_of_class(Haunt)

    def _get_perms_of_class(self, c):
        return [p for p in self._play if isinstance(p,c)]

    #IO

    #displays the player's resources, agenst, haunts, public hand and hand
    #allows assinging keys to display with any item in any of those lists
    #private: toggles on private view (hand, private resources, hidden permanents)
    def getDispText(self, private : bool, keyList : {id : object} = {}):

        def listCards(cards, cols = 2):
            text = ""
            num = 0
            l = len(cards) #last index
            for card in sorted(cards):
                text += "\t" 
                if id(card) in keyList.keys():
                    text += str(keyList[id(card)]) + ": "
                text += card.getDispText(private)
                num += 1
                if num % cols == 0 and num  < l:
                    #newline after every N cols, but never at the end of the list
                    text += "\n"
            return text

        #HEADER
        text = "~~"+self._name + "~ " +self._gold.getDispText(self.goldAcc, private) + " ~ " + self._clues.getDispText(self.cluesAcc, private)+" ~~\n"
        #CARDS
        text += "AGENTS:\n"
        text += listCards(self.getAgents())
        text += "\nHAUNTS:\n"
        text += listCards(self.getHaunts())
        text += "\nPUBLIC HAND: (cards may no longer be in hand)\n"
        text += listCards(self._pub_hand)
        text += "HAND:\n"
        if private:
            text += listCards(self._hand)
        else:
            text += "\t~~"+str(len(self._hand))+" Cards~~"
        return text

    #GAME LOGIC

    def gen(self):
        for haunt in self.getHaunts():
            self._gold.add(haunt.gen(), False, haunt)

    def draw(self, n = 1):
        self._hand.extend(self._deck.draw(n))

    def discard(self, card):
        self._hand.remove(card)

    def turn(self):
        for p in self._play:
            if p.turn:
                p.turn()

    """ #REMOVED
    def canPlay(self, card):
        return card.canPlay(self._gold)

    def play(self, card, costPaid):
        card.play(self._play,costPaid)
        self._gold.add(-1*costPaid,True) 

    def spy(self, agent : Agent):
        self._clues.add(agent.spy(), False, agent)

    def thieve(self, agent : Agent):
        self._gold.add(agent.thieve(), False, agent)
    #process the outcomes of an action taken by an agent
    def processOutcomes(self, oc : ActionOutcome):
        self._gold.add(oc.gold, oc.public) 
        self._clues.add(oc.clues, oc.public)
        for card in (c for c in oc.deathList if c in self._play):
            card.die()
            oc.remove(card)
        self._play += oc.spawnList
        for card in oc.discardList: 
            self._hand.remove(card)
            oc.discardList.remove(card) 
        for agent in oc.revealList:
            self.reveal(agent)
        self.draw(oc.drawCount)
    """
        
    def gainResource(self, resource : str, public, source, val):
        if resource == self.goldAcc:
            self._gold.add(val, public, source)
        if resource == self.cluesAcc:
            self._clues.add(val, public, source)

    def spawn(self, permanent):
        self._play.append(permanent)

    def kill(self, permanent):
        permanent.die()
    
    def reveal(self, agent):
        agent.reveal()
        self._clues.reveal(agent)
        self._gold.reveal(agent)
        self._pub_hand.remove(agent)

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
                self._tracked_priv[id(source)] += val

        #make all tracked private changes from a source public
        def reveal(self, source):
            self._pub += self._tracked_priv[id(source)]
            del self._tracked_priv[id(source)]

        def getDispText(self, accronym, private):
            return (str(self.priv()) if private else "?") + accronym +" ("+str(self.pub())+ accronym + " Public)"