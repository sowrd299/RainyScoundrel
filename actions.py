#DEPRICATED

#MAIN TURN ACTIONS

#a class to represent arguments to actions
class Arg():

    def __init__(self, name, t : type, friendly : bool):
        self._name = name
        self._type = t #what type of data to input
        self._friendly = friendly #to collect from a friendly or enemy player


class Action():

    def __init__(self, name, action ):
        self.go = action
        self._name = name

    def getDispText(self):
        return self._name