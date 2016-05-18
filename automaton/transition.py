class Transition(object):

    def __init__(self, val, to):
        self.val = val
        self.setTo(to)
        self.weight = 0

    def setTo(self, to):
        self.to = to
        to.addiTransition(self)

    def setFrom(self, fro):
        self.fro = fro

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def getTo(self):
        return self.to

    def getFrom(self):
        return self.fro

    def getVal(self):
        return self.val

    def getlCost(self):
        return self.fro.getlCost()+self.weight

    def getrCost(self):
        return self.to.getrCost()+self.weight

    def isOptimal(self):
        return self.fro.getrCost() == (self.weight+self.to.getrCost())

    def getCost(self):
        return self.fro.getlCost()+self.weight+self.to.getrCost()
