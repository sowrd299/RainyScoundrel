import cards
import game
from decks import Deck 
from textBasedPlayerControllers import TextBasedPC

#GAME SETTING CONSTANTS
numPlayers = 2

#text display
title = "~~THIEVES, SCOUNDRLES and SPIES~~"
subtitle = "A game of covert opperations in the underbelly of the city."

def printTitle():
    print("\n"+title)
    print(subtitle)
    print("~" * len(title) + "\n")

def getTestingDeck():
    r = []
    r.append(cards.AgentCard("Sleuth",4,4,2,2))
    r.append(cards.AgentCard("Pick-Pocket",1,0,1,2))
    r.append(cards.AgentCard("Thug",2,1,3,1))
    r.append(cards.AgentCard("Big Thug",3,1,4,2))
    r.append(cards.AgentCard("Sleuth",4,4,2,2))
    r.append(cards.AgentCard("Pick-Pocket",1,0,1,2))
    r.append(cards.AgentCard("Thug",2,1,3,1))
    r.append(cards.AgentCard("Big Thug",3,1,4,2))
    return Deck(r)

def main():
    printTitle()
    g = game.Game( [getTestingDeck() for i in range(numPlayers)], [TextBasedPC for i in range(numPlayers)] )
    while g.main():
        printTitle()

if __name__ == "__main__":
    main()
    input()