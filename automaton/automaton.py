class Automaton(object):

    def __init__(self, initialState):
        self.initialState = initialState
        self.states = dict()
        self.selection = dict()
        self.interpretations = list()
        self.restorations = set()
        self.build(self.initialState)

    def build(self, state):
        if state.getVariable() == '':
            self.finalState = state
        else:
            self.insertState(state)
        for t in state.getoTransitions():
            self.build(t.getTo())

    def insertState(self, state):
        key = state.getVariable()
        if key not in self.states:
            self.states[key] = list()
        if state not in self.states[key]:
            self.states[key].append(state)

    def addSelection(self, key, val):
        self.selection[key] = val
        for state in self.states[key]:
            state.update(val)

    def removeSelection(self, key):
        del self.selection[key]
        for state in self.states[key]:
            state.relax()

    def getInitialState(self):
        return self.initialState

    def getFinalState(self):
        return self.finalState

    def showRestoration(self):
        i = 1
        for restoration in self.restorations:
            print('Solution ' + str(i))
            for key in restoration.split(' '):
                print('UNDO: ' + key + ' - ' + self.selection[key])
                print('------------')
            i+=1

    def develop(self, state, e, relax):
        if state is self.finalState:
            self.interpretations.append(e.lstrip())
            self.restorations.add(relax.lstrip())
        h = state.getVariable()
        for transition in state.getoTransitions():
            if transition.isOptimal():
                if transition.getWeight() > 0:
                    self.develop(transition.getTo(), e + ' ' + h + ' - /', relax + ' ' + h)
                else:
                    self.develop(transition.getTo(), e + ' ' + h + ' - ' + transition.getVal(), relax)

    def isConsistent(self):
        return self.finalState.getlCost() == 0