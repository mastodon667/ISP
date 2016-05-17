__author__ = 'Herbert'

class State(object):

    def __init__(self, variable, importance):
        self.variable = variable
        self.importance = importance
        self.lCost = 0
        self.rCost = 0
        self.iTransitions = list()
        self.oTransitions = list()
        self.counts = dict()

    def addoTransition(self, transition):
        self.oTransitions.append(transition)
        transition.setFrom(self)
        count = 1
        if transition.getVal() in self.counts:
            count += self.counts[transition.getVal()]
        self.counts[transition.getVal()] = count

    def addiTransition(self, transition):
        self.iTransitions.append(transition)

    def getoTransitions(self):
        return self.oTransitions

    def getiTransitions(self):
        return self.iTransitions

    def getVariable(self):
        return self.variable

    def getlCost(self):
        return self.lCost

    def getrCost(self):
        return self.rCost

    def update(self, val):
        for transition in self.oTransitions:
            if val != transition.getVal():
                transition.setWeight(self.importance)
            else:
                transition.setWeight(0)
            transition.getTo().recalculatelCost()
        self.recalculaterCost()

    def relax(self):
        for transition in self.oTransitions:
            transition.setWeight(0)
            transition.getTo().recalculatelCost()
        self.recalculaterCost()

    def recalculaterCost(self):
        r = self.calculaterCost()
        if r != self.rCost:
            self.rCost = r
            for transition in self.iTransitions:
                transition.getFrom().recalculaterCost()
        self.updateCounts()

    def updateCounts(self):
        for char in self.counts:
            t = 0
            for transition in self.oTransitions:
                if transition.getVal() == char:
                    if transition.getCost() == 0:
                        t+=1
            self.counts[char] = t

    def recalculatelCost(self):
        l = self.calculatelCost()
        if l != self.lCost:
            self.lCost = l
            for transition in self.oTransitions:
                transition.getTo().recalculatelCost()
        self.updateCounts()

    def calculatelCost(self):
        cost = 1000 #WARNING: MAY CAUSE ERRORS
        for transition in self.iTransitions:
            c = t.getlCost()
            if c < cost:
                cost = c
        return cost

    def calculaterCost(self):
        cost = 1000 #WARNING: MAY CAUSE ERRORS
        for transition in self.oTransitions:
            c = t.getrCost()
            if c < cost:
                cost = c
        return cost

    def getoTransition(self, val):
        for transition in self.oTransitions:
            if transition.getVal() == val:
                return transition
        return None