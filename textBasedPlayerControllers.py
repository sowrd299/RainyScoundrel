from absPlayerControllers import PlayerController

class TextBasedPC(PlayerController):

    def chooseFromCards(self, choices, endTurn = True):
        count = iter(range(len(choices)+1))
        print(self._game.getDispText( {"keyList" : {id(card) : next(count) for card in choices}} ))
        if endTurn:
            print("\n"+str(next(count))+": End Turn")
            choices.append(self._game.actionEndTurn)
        return self._chooseByIndex("Choose a card (by index)", choices)

    def chooseFromList(self, choices):
        count = iter(range(len(choices)))
        for item in choices:
            print(str(next(count)) + ": " + item.getDispText())
        return self._chooseByIndex("Choose and action", choices) #TODO: make this more reusable

    def _chooseByIndex(self, prompt, choices):
        choice = input(prompt+": ")
        try:
            return choices[int(choice)]
        except TypeError:
            return None
        except IndexError:
            return None

    def chooseNumber(self, prompt, pred):
        while True:
            choice = input(prompt + ": ")
            try:
                if pred(int(choice)):
                    return int(choice)
                else:
                    print("That number is not valid.")
            except TypeError:
                print("You must input a number.")