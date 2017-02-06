import pygame
import math
import random
from q_node import Node

def validNode(q):
    if q[0] in range(0, width) and q[1] in range(0, height):
        if image.get_at(q) == pygame.Color(0, 0, 0, 255):
            return False
        else:
            return True
    else:
        return False


def endOfTheLine(q, radius):
    for i1 in range(q.getIntCoord()[0] - radius, q.getIntCoord()[0] + radius):
        for j1 in range(q.getIntCoord()[1] - radius, q.getIntCoord()[1] + radius):
            if i1 in range(0, width) and j1 in range(0, height):
                if not validNode((i1, j1)):
                    return True

def genSuccessors(q, step):
    (x, y) = q.getCoord()
    return [Node(x+step, y), Node(x-step, y), Node(x, y+step), Node(x, y-step)]

initial_node = Node(305, 5)
goal = Node(300, 300)

closed_list = []
open_list = [initial_node]
delta = 3.25
finished = False

while not finished:
    if open_list:
        current_node = open_list[0]
    else:
        break

    index = 0
    for n in range(0, len(open_list)):
        if open_list[n].getHCost() < current_node.getHCost():
            current_node = open_list[n]
            index = n

    successors = genSuccessors(current_node, delta)

    for s in successors:
        s.setParent(current_node)
        s.setH(s.distance(goal)**2)
        if endOfTheLine(s, int(2)):
            continue

        the_list = open_list + closed_list

        for node in the_list:
            if node.getCoord() == s.getCoord() and node.getHCost() <= s.getHCost():
                break
        else:
            open_list.append(s)

        if s.getIntCoord()[0] in range(goal.getIntCoord()[0]-int(delta), goal.getIntCoord()[0]+int(delta)) and s.getIntCoord()[1] in range(goal.getIntCoord()[1]-int(delta), goal.getIntCoord()[1]+int(delta)):
            finished = False

    closed_list.append(open_list.pop(index))

