import haunts #for use with preventable actions

#MAIN TURN ACTIONS

#An error to be thrown when an action attempt to execute
#   before all its args have been filled
class UnfilledActionArgError(Exception):
    pass

#A class to represent arguments to actions
class ActionArg():

    def __init__(self, name, t : type, pred = (lambda x : True), friendly = True, opt = False, dispText = ""):
        self._name = name #Brief description of the value
        self._type = t #what type of data to input
        self._pred = pred #further specifications about the value
        self._friendly = friendly #to collect from a friendly or enemy player
        self._opt = opt #if the arguement is optional
        self._dispText = dispText
        self._val = None

    def getType(self):
        return self._type

    def getDispText(self):
        return self._dispText or self._name

    def getFriendly(self):
        return self._friendly

    #set the value of the argument to the given value
    #only allows arguments legal by the given standards
    #returns succes status
    def setVal(self, val):
        if isinstance(val, self._type) and self._pred(val):
            self._val = val
            return True
        return False

    #returns the current value of the argument
    #errors in the argument has not been set yet
    def getVal(self):
        if self._val == None and not self._opt:
            raise UnfilledActionArgError("Must set argument: "+self._name)
        return self._val


#Carries data from card action to player
#TODO: improve scalability of this system
class ActionOutcome():
    
    def __init__(self, public = True, gold = 0, clues = 0, deathList = [], spawnList = [], discardList = [], revealList = [], drawCount = 0):
        self.public = public
        self.gold = gold #gold earned/spend
        self.clues = clues #clues earned/spent
        self.deathList = deathList #permanents that died
        self.spawnList = spawnList #permanents that died
        self.discardList = discardList #cards in hand no longer in hand
        self.revealList = revealList #hidden permanents to be revealed
        self.drawCount = drawCount #number of cards to draw


#An attaction (usually attached to a specific card)
#   that a player can preform
class Action():

    def __init__(self, name : str, action, args : [ActionArg], public : bool, outcomeType : str):
        self._name = name #the name of the action
        self._action = action #the function that resolves the action
        self._args = args #the list of arguments to the action
        self._public = public #if the action is public
        self._outcomeType = outcomeType #what type of result the action has
                                        #   can be: "gold", "clues", "deathList", "spawnList"

    def getDispText(self):
        return self._name

    def getArgs(self):
        return list(self._args) #return copy to prevent mutation

    #formats the output from the raw output of the action
    #   to an ActionOutcome object
    def _formatOutcome(self, oc):
        return eval("ActionOutcome(self._public, "+self._outcomeType+" = oc)")

    #Preforms the action
    #Raises "UnfilledActionArgError" if premature
    def go(self):
        oc = self._action( *(arg.getVal() for arg in self._args) )
        return self._formatOutcome(oc)


#a class to represent actions enemy players can prevent
class PreventableAction(Action):

    _promptText = "Select a "+haunts.Haunt.typeName+" to hide in to prevent this action"
    _disclaimer = " (can be prevented)" 
    _prevOutcome = ActionOutcome(False)

    def __init__(self, name, action, preventedAction, args, public, outcomeType):
        Action.__init__(self, name, action, args, public, outcomeType)
        self._prevArg = ActionArg(haunts.preventName, haunts.Haunt, friendly = False, opt = True, dispText = self._promptText)
        self._prevAction = preventedAction # the action to preform when the main action is prevented
    
    def getDispText(self):
        return Action.getDispText(self) + self._disclaimer

    def getArgs(self):
        return  Action.getArgs(self) + [self._prevArg]

    def go(self):
        prevHaunt = self._prevArg.getVal()
        if prevHaunt:
            prevHaunt.prevent(self)
            self._prevAction()
            return self._prevOutcome
        return Action.go(self)