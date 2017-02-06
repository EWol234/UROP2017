import math, sys

class Node(object):
    def __init__(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor
        self.parent = None
        self.children = []
        self.cost = 0
        self.endNode = False
        self.h = 0

    def getCoord(self):
        return (self.xcor, self.ycor)

    def getIntCoord(self):
        return (int(self.xcor), int(self.ycor))

    def getCost(self):
        return self.cost

    def isEnd(self):
        return self.endNode

    def setEnd(self, en):
        self.h = 100
        if self.getParent() is not False:
            self.getParent().setEnd(True)

    def setParent(self, parent_node):
        self.parent = parent_node
        parent_node.addChild(self)
        self.cost = self.parent.getCost() + self.distance(self.parent)

    def setCost(self, cost):
        self.cost = cost

    def addChild(self, child_node):
        self.children.append(child_node)

    def getHCost(self):
        return self.cost + self.h

    def distance(self, qnode):
        return math.sqrt((self.xcor-qnode.getCoord()[0])**2 + (self.ycor-qnode.getCoord()[1])**2)

    def getChildren(self):
        return self.children

    def getParent(self):
        if self.parent is not None:
            return self.parent
        else:
            return False

    def getH(self):
        return self.h

    def setH(self, h):
        self.h = h
