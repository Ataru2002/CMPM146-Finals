from mctsNode import MCTSNode
from gameMaze import gameMaze
import constants
import copy
from random import choice
from math import sqrt, log

numNodes = 1000
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


def heuristicBot(maze: gameMaze):
    # Heuristic #1: If the bot can reach the goal faster than the player, simply go for it

    botPath = maze.BFS(maze.getPosBot(), maze.end)
    playerPath = maze.BFS(maze.getPosPlayer(), maze.end)

    if playerPath == None or botPath == None:
        print("current Maze")
        print(maze.graph[maze.getPosPlayer()])
        print(botPath)
        maze.getStringMaze()
    elif playerPath == None or len(botPath) < len(playerPath):
        path = botPath
        return path[1]
    

    # Heuristic #2: Check if the Bot can block any of the path faster than the player can reach it
    lenchosen = 1000000000
    chosen = None
    for i in maze.mapping:
        if maze.mapping[i][0] == 0:
            paths_bot = maze.BFS(maze.getPosBot(), i) #Path from the bot to the lever
            paths_player = maze.BFS(maze.getPosPlayer(), maze.mapping[i][1]) #Path from the player to the wall the lever is associated with
            if paths_bot != None and paths_player != None and len(paths_bot) < len(paths_player):
                if lenchosen > len(paths_bot):
                    chosen = paths_bot
                    lenchosen = len(paths_bot)
    if lenchosen < 1000000000:
        return chosen[1]
    return chosen
            
def heuristicPlayer(maze: gameMaze):
    '''
    pathToBot = maze.BFS(maze.getPosPlayer(), maze.getPosBot())
    pathToEnd = maze.BFS(maze.getPosPlayer(), maze.end)

    if pathToBot == None and pathToEnd == None:
        return None
    
    if len(pathToBot) < len(pathToEnd):
        return pathToBot[1]
    if len(pathToBot) >= len(pathToEnd):
        return pathToEnd[1]
    '''
    botPath = maze.BFS(maze.getPosBot(), maze.end)
    playerPath = maze.BFS(maze.getPosPlayer(), maze.end)

    if playerPath == None or botPath == None:
        print("current Maze")
        print(maze.graph[maze.getPosPlayer()])
        print(botPath)
        maze.getStringMaze()
    elif botPath == None or len(botPath) > len(playerPath):
        path = playerPath
        return path[1]
    

    # Heuristic #2: Check if the Player can block any of the path faster than the Bot can reach it
    lenchosen = 1000000000
    chosen = None
    for i in maze.mapping:
        if maze.mapping[i][0] == 0:
            paths_player = maze.BFS(maze.getPosPlayer(), i) #Path from the Player to the lever
            paths_bot = maze.BFS(maze.getPosBot(), maze.mapping[i][1]) #Path from the Bot to the wall the lever is associated with
            if paths_bot != None and paths_player != None and len(paths_bot) > len(paths_player):
                if lenchosen > len(paths_player):
                    chosen = paths_player
                    lenchosen = len(paths_player)
    if lenchosen < 1000000000:
        return chosen[1]
    return chosen

def rollout(maze: gameMaze, state):
    while not maze.isTerminal():
        chosenMove = heuristicBot(maze)
        if chosenMove == None:
            chosenMove = choice(maze.getLegalActions(state))
        maze.updatePos(chosenMove, constants.USER_BOT)

        chosenMovePlayer = heuristicPlayer(maze)
        if chosenMovePlayer == None:
            chosenMovePlayer = choice(maze.getLegalActions(maze.getPosPlayer()))
        maze.updatePos(chosenMovePlayer, constants.USER_PLAYER)
        state = maze.getPosBot()
    return state

def backpropagate(node: MCTSNode, won: bool):
    '''
    current = node
    while current.parent != None:
        node.wins += won
        node.visits += 1
        current = current.parent
    '''
    node.visits += 1
    if node.parent == None: 
        return
    node.wins += won
    backpropagate(node.parent, won)

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
    explore = exploreFaction * sqrt(natural_log / (node.visits))
    return exploit + explore

def getBestAction(root: MCTSNode, previous):
    '''
    next_node = choice(list(root.child_nodes.values()))
    maxwr = 0
    for child in root.child_nodes.values():
        wr = child.wins / child.visits
        if wr > maxwr:
            maxwr = wr
            next_node = child
    return next_node.parent_action
    '''
    val = -1000000000
    visit = -1
    chosen_move = None
    # Finding the node with the maximum UCT
    for instances in root.child_nodes.keys():
        print(root.child_nodes[instances], root.child_nodes[instances].wins / root.child_nodes[instances].visits)
        if root.child_nodes[instances].wins / root.child_nodes[instances].visits > val:
            if root.child_nodes[instances].visits > visit:
                val = root.child_nodes[instances].wins / root.child_nodes[instances].visits
                visit = root.child_nodes[instances].visits
                chosen_move = instances
    
    for instances in root.child_nodes.keys():
        if root.child_nodes[instances].wins / root.child_nodes[instances].visits == val:
            if len(previous) < 5:
                previous.append(instances)
            else:
                if instances not in previous:
                    previous.append(instances)
                    chosen_move = instances
                    del previous[0]
    return chosen_move

def think(maze: gameMaze, currentState, previous):
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
        #copyMaze.getStringMaze()
        backpropagate(node, (copyMaze.winner() == 1))
        #print("---------------------------------------------")


    #print(maze.getPosBot(), maze.getPosPlayer())
    best_action = getBestAction(rootNode, previous)
    print(f"Action chosen: {best_action}")
    return best_action

#maze = gameMaze("./maze1.txt")

#think(maze, maze.getPosBot())