from absPlayerControllers import PlayerController

class TextBasedPC(PlayerController):

    def chooseFromCards(self, choices, endTurn = True):
        choices.sort()
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
        except ValueError:
            print("That is not a valid index.")
            return None
        except IndexError:
            print("That index is out of range.")
            return None

    def chooseNumber(self, prompt, pred):
        while True:
            choice = input(prompt + ": ")
            try:
                if pred(int(choice)):
                    return int(choice)
                else:
                    print("That number is not valid.")
            except ValueError:
                print("You must input a number.")

    #TODO: Implement reports
    #TODO: Implement choosing to prevent