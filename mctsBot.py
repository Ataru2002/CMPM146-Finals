from mctsNode import MCTSNode
from gameMaze import gameMaze
import constants
import random
from math import sqrt, log

numNodes = 100
exploreFaction = 2.

# TODO: how is a "state" represented?
def traverseNodes(node: MCTSNode, maze: gameMaze, state):
    pass

def expandLeaf(node: MCTSNode, maze: gameMaze, state):
    pass

def rollout(maze: gameMaze, state):
    pass

def backpropagate(node: MCTSNode, won: bool):
    current = node
    while (current):
        node.wins += 1 if won else 0
        node.visits += 1
        
        current = current.parent

def ucb(node: MCTSNode):
    win_rate = node.wins / node.visits
    explore = exploreFaction * sqrt((log(node.parent.visits) / node.visits))
    return win_rate + explore

def getBestAction(root: MCTSNode):
    pass

def think(maze: gameMaze, currentState):
    pass