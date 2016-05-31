#LOCATION = '/home/herbert/PycharmProjects/Thesis/idp/'
LOCATION = 'C:/Users/Herbert/PycharmProjects/ISP/'

import time

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

    def getAllChoices(self):
        return self.selection

    def getSelection(self, key):
        return self.selection[key]

    def insertState(self, state):
        key = state.getVariable()
        if key not in self.states:
            self.states[key] = list()
        if state not in self.states[key]:
            self.states[key].append(state)

    def addSelection(self, key, val):
        if key in self.selection:
            self.removeSelection(key)
        self.selection[key] = val
        ts = time.time()
        for state in self.states[key]:
            state.update(val)
        te = time.time()
        with open(LOCATION + 'reader/results.txt', 'a') as file:
            file.write('insertion - ' + str(te - ts) + '\n')

    def removeSelection(self, key):
        if key in self.selection:
            del self.selection[key]
            ts = time.time()
            for state in self.states[key]:
                state.relax()
            te = time.time()
            with open(LOCATION + 'reader/results.txt', 'a') as file:
                file.write('insertion - ' + str(te - ts) + '\n')

    def getInitialState(self):
        return self.initialState

    def getFinalState(self):
        return self.finalState

    def calculateRestorations(self):
        self.interpretations = list()
        self.restorations = set()
        ts = time.time()
        self.develop(self.initialState, '', '')
        te = time.time()
        with open(LOCATION + 'reader/results.txt', 'a') as file:
            file.write('solutions - ' + str(te - ts) + '\n')
        return self.restorations

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
        ts = time.time()
        c = self.finalState.getlCost() == 0
        te = time.time()
        with open(LOCATION + 'reader/results.txt', 'a') as file:
            file.write('sat - ' + str(te - ts) + '\n')
        return c
