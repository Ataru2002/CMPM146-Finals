from mctsNode import MCTSNode
from gameMaze import gameMaze
import constants
import copy
from random import choice
from math import sqrt, log

numNodes = 100
exploreFaction = 2
naturalNumber = 2.71828

# TODO: how is a "state" represented?
def traverseNodes(node: MCTSNode, maze: gameMaze, state):
    # Start from the root
    starter = node

    # Traversal
    currentBoard = maze
    while(starter.untried_actions == [] and not currentBoard.isTerminal()):
        uct_val = -1000000000
        chosen_node = None
        chosen_move = None
        for instances in starter.child_nodes.keys():
            if ucb(starter.child_nodes[instances]) > uct_val:
                uct_val = ucb(starter.child_nodes[instances])
                chosen_node = starter.child_nodes[instances]
                chosen_move = instances
        starter = chosen_node
        # 1 is here because it's the bot, although might need to see if we need to implement the MCTS for 2 players instead of 1
        #print("Chosen move is: ", chosen_move)
        #print("Current position of the bot: ", maze.getPosBot())
        currentBoard.updatePos(chosen_move, constants.USER_BOT)
        
    return starter, maze.getPosBot()

def expandLeaf(node: MCTSNode, maze: gameMaze, state):
    if node.untried_actions == [] and node.child_nodes:
        return node, state
    #print("untried",node.untried_actions)
    randmove = choice(node.untried_actions)
    maze.updatePos(randmove, constants.USER_BOT)
    next_node = MCTSNode(parent=node, parent_action=randmove, action_list=maze.getLegalActions(maze.getPosBot()))
    
    # remove the move from list of untried moves
    node.untried_actions.remove(randmove)
    node.child_nodes[randmove] = next_node
    #print("move chosen in expand_leaf: ", randmove)
    return next_node, maze.getPosBot()

def rollout(maze: gameMaze, state):
    while not maze.isTerminal():
        chosenMove = choice(maze.getLegalActions(state))
        #print(chosenMove, maze.getPosBot())
        maze.updatePos(chosenMove, constants.USER_BOT)
        state = maze.getPosBot()
    return state

def backpropagate(node: MCTSNode, won: bool):
    current = node
    while (current):
        node.wins += won
        node.visits += 1
        current = current.parent

def ucb(node: MCTSNode):
    '''
    win_rate = node.wins / node.visits
    explore = exploreFaction * sqrt((log(node.parent.visits) / node.visits))
    return win_rate + explore
    '''
    if node.parent == None:
        # root node
        return -1 
    natural_log = log(node.parent.visits + 1) / log(naturalNumber)
    exploit = (node.wins / (node.visits + 1))
    explore = exploreFaction * sqrt(natural_log / (node.visits + 1))
    return exploit + explore

def getBestAction(root: MCTSNode):
    next_node = choice(list(root.child_nodes.values()))
    maxwr = 0

    for child in root.child_nodes.values():
        wr = child.wins / child.visits

        if wr > maxwr:
            maxwr = wr
            next_node = child
    return next_node.parent_action

def think(maze: gameMaze, currentState):
    # The state in this context would be the bot's position
    rootNode = MCTSNode(parent=None, parent_action=None, action_list=maze.getLegalActions(currentState))
    for _ in range(numNodes):
        copyMaze = copy.deepcopy(maze)
        state = currentState
        node = rootNode 
        #print("New Maze Pos: ", copyMaze.getPosBot())
        node, state = traverseNodes(node, copyMaze, state)
        #print("New Maze Pos: ", copyMaze.getPosBot())
        #print("after traverse: ", node, state)
        node, state = expandLeaf(node, copyMaze, state)
        #print("New Maze Pos: ", copyMaze.getPosBot())
        #print("after expand: ", node, state)
        state = rollout(copyMaze, state)
        backpropagate(node, (copyMaze.winner() == 1))
        #print("---------------------------------------------")


    print(maze.getPosBot(), maze.getPosPlayer())
    best_action = getBestAction(rootNode)
    print(f"Action chosen: {best_action}")
    return best_action

#maze = gameMaze("./maze1.txt")

#think(maze, maze.getPosBot())