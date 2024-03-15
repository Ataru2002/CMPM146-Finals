# a class that stores the following:
# 2D array representation x
# string array that stores the entire maze x
# a function that prints out the entire maze when called x
# graph representation of the maze x
# states (Where the player is right now, where the bot is right now) x
# states that can't be mutate (i.e where the levers, openable walls, start points, end points, etc) x
# TODO: how to specify which levers trigger which walls
# FIXME: when player and bot move to the same tile, the game doesn't end
import constants

class gameMaze:
    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                # parse maze.txt file into self.grid
                content = file.read()
                self.grid = []
                current = []
                for i in content:
                    if i != '\n':
                        current.append(i)
                    if i == '\n':
                        self.grid.append(current)
                        current = []

                # initialize special tiles
                self.levers = []
                self.openWalls = []
                for i in range(0, len(self.grid)):
                    for j in range(0, len(self.grid)):
                        if self.grid[i][j] == constants.PLAYER:
                            self.player = (i, j)
                        if self.grid[i][j] == constants.BOT:
                            self.bot = (i, j)
                        if self.grid[i][j] == constants.END:
                            self.end = (i, j)
                        if self.grid[i][j] == constants.LEVER:
                            self.levers.append((i, j))
                        if self.grid[i][j] == constants.OPEN_WALL:
                            self.openWalls.append((i, j))

        except FileNotFoundError:
            print(f"File not found: {filename}")
            input()
            quit()

        self.graph = {} # graph form of the maze
        self.mapping = {} # mapping of levers and openable walls
        # constants.USER_PLAYER = 0, constants.USER_BOT = 1
        self.currentPlayer = -1

        # initialize graph form of the maze
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] != constants.WALL:
                    self.graph[(i, j)] = []
                    if i > 0 and self.grid[i - 1][j] != constants.WALL:
                        self.graph[(i, j)].append((i - 1, j))
                    if i < len(self.grid) - 1 and self.grid[i + 1][j] != constants.WALL:
                        self.graph[(i, j)].append((i + 1, j))
                    if j > 0 and self.grid[i][j - 1] != constants.WALL:
                        self.graph[(i, j)].append((i, j - 1))
                    if j < len(self.grid) - 1 and self.grid[i][j + 1] != constants.WALL:
                        self.graph[(i, j)].append((i, j + 1))

        # ideally lever and openable walls should have the same size
        # self.mapping[]
        for i in range(0, len(self.levers)):
            # 0 means off, 1 means on
            self.mapping[self.levers[i]] = (0, self.openWalls[i])
        #print(self.mapping)

    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getGridMaze(self):
        print(self.grid)

    def getGraphMaze(self):
        print(self.graph)

    def getStringMaze(self):
        output = ""
        for instances in self.grid:
            for j in instances:
                output += j
            output += "\n"
        print(output)

    
    # Output a path from start to goal in the maze (assuming both are empty spaces), else returns None
    def BFS(self, start, goal):
        visited = {}
        queue = []
        visited[start] = None
        queue.append(start) # what is the start node?
        while queue:
            node = queue.pop()
            if node == goal:
                return createPath(start, goal, visited) # are we returning the path from start to end?
            else:
                for new_node in self.graph[node]:
                    if new_node not in visited:
                        visited[new_node] = node
                        queue.append(new_node)
        return None
    
    # Returns if it's possible to go from currentPos to newPos
    def checkLegal(self, currentPos, newPos):
        if abs(currentPos[0] - newPos[0]) == 1 and currentPos[1] != newPos[1]:
            print("Illegal move: bad movement")
            return False # Can only move up down
        if abs(currentPos[1] - newPos[1]) == 1 and currentPos[0] != newPos[0]:
            print("Illegal move: bad movement")
            return False # Can only move left right
        if abs(currentPos[1] - newPos[1]) > 1 or abs(currentPos[0] - newPos[0]) > 1:
            print("Illegal move: bad movement")
            return False # Moves too far
        if self.grid[newPos[0]][newPos[1]] == constants.WALL:
            print("Illegal move: hitting a wall")
            return False # Can only move in empty spaces, not walls
        return True

    # Updates the position of currentPlayer to newPos, if possible. Returns True if successful, else returns False.
    def updatePos(self, newPos, currentPlayer):
        oldPos = None
        if currentPlayer == constants.USER_PLAYER:
            oldPos = (self.player[0], self.player[1])
        else:
            oldPos = (self.bot[0], self.bot[1])

        if not self.checkLegal(oldPos, newPos):
            return False
        if oldPos in self.levers:
            self.grid[oldPos[0]][oldPos[1]] = constants.LEVER
        elif oldPos in self.openWalls:
            self.grid[oldPos[0]][oldPos[1]] = constants.OPEN_WALL
        else:
            self.grid[oldPos[0]][oldPos[1]] = constants.PATH

        if self.grid[newPos[0]][newPos[1]] == constants.LEVER:
            self.toggleLever(newPos)
        
        # 0 means player, 1 means bot
        if currentPlayer == constants.USER_PLAYER:
            self.grid[newPos[0]][newPos[1]] = constants.PLAYER
            self.player = newPos      
        else:
            self.grid[newPos[0]][newPos[1]] = constants.BOT
            self.bot = newPos   
        return True
    
    # Toggles the lever at leverPos.
    def toggleLever(self, leverPos):
        active, targetWall = self.mapping[leverPos]
        if active == 0:
            # convert the openable wall into a grid
            self.grid[targetWall[0]][targetWall[1]] = constants.WALL
            # updating the graph
            for i in self.graph[targetWall]:
                self.graph[i] = set(self.graph[i])
                self.graph[i].discard(targetWall)
                self.graph[i] = list(self.graph[i])
            del self.graph[targetWall]
            self.mapping[leverPos] = (1, targetWall)
        elif active == 1:
            # convert the openable wall into a grid
            self.grid[targetWall[0]][targetWall[1]] = constants.OPEN_WALL
            # updating the graph
            self.graph[targetWall] = []
            i,j = targetWall
            if i > 0 and self.grid[i - 1][j] != constants.WALL:
                self.graph[targetWall].append((i - 1, j))
            if i < len(self.grid) - 1 and self.grid[i + 1][j] != constants.WALL:
                self.graph[targetWall].append((i + 1, j))
            if j > 0 and self.grid[i][j - 1] != constants.WALL:
                self.graph[targetWall].append((i, j - 1))
            if j < len(self.grid) - 1 and self.grid[i][j + 1] != constants.WALL:
                self.graph[targetWall].append((i, j + 1))
            self.mapping[leverPos] = (0, targetWall)

    # Returns True if the game has ended.
    def isTerminal(self):
        return (self.player == self.bot) or (self.player == self.end) or (self.bot == self.end)
        # endgame = False
        # if (self.player == self.bot) or (self.player == self.end):
        #     endgame = True
        # if self.bot == self.end:
        #     endgame = True
        # return endgame
    
    # Returns 0 if the player won, 1 if the bot won, or -1 if the game has not ended.
    def winner(self):
        if not self.isTerminal():
            return -1
        if (self.player == self.bot) or (self.player == self.end):
            return constants.USER_PLAYER
        if self.bot == self.end:
            return constants.USER_BOT
    
    # Returns a list of legal moves at currentPos.
    def getLegalActions(self, currentPos):
        i, j = currentPos[0], currentPos[1]
        output = []
        if i > 0 and self.grid[i - 1][j] != constants.WALL:
            output.append((i - 1, j))
        if i < len(self.grid) - 1 and self.grid[i + 1][j] != constants.WALL:
            output.append((i + 1, j))
        if j > 0 and self.grid[i][j - 1] != constants.WALL:
            output.append((i, j - 1))
        if j < len(self.grid) - 1 and self.grid[i][j + 1] != constants.WALL:
            output.append((i, j + 1))
        return output

def createPath(start, goal, visited):
        path = [goal]
        current = goal
        while(current != start):
            path.append(visited[current])
            current = visited[current]
        path.reverse()
        return path