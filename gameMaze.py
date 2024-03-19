# a class that stores the following:
# 2D array representation x
# string array that stores the entire maze x
# a function that prints out the entire maze when called x
# graph representation of the maze x
# states (Where the player is right now, where the bot is right now) x
# states that can't be mutate (i.e where the levers, openable walls, start points, end points, etc) x
# FIXME: when player and bot move to the same tile, the game doesn't end
import constants

class gameMaze:
    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                # initialize self.grid
                self.grid = []
                
                content = file.readline()
                current = []
                while (content != "\n"):
                    for i in content:
                        if i != '\n':
                            current.append(i)
                    self.grid.append(current)
                    current = []
                    
                    content = file.readline()
                
                # save lever mapping for later
                contentLevers = file.readlines()
                    
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
            quit()
        
        self.currentPlayer = -1

        # initialize graph form of the maze
        self.graph = {}
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
        
        # initialize lever-to-wall mapping
        self.mapping = {}
        for l in contentLevers:
            leverY, leverX, wallY, wallX = l.split()
            new_lever = (int(leverY), int(leverX))
            new_wall = (int(wallY), int(wallX))
            
            if new_lever not in self.levers:
                print(f"ERROR: ({leverY}, {leverX}) is not a real lever.")
                quit()
                
            if new_wall not in self.openWalls:
                print(f"ERROR: ({wallY}, {wallX}) is not a real openable wall.")
                quit()
                
            self.mapping[new_lever] = (0, new_wall)

    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPosBot(self):
        return self.bot
    
    def getPosPlayer(self):
        return self.player

    def getGridMaze(self):
        print(self.grid)

    def getGraphMaze(self):
        print(self.graph)

    def getStringMaze(self):
        output = ""
        
        # find lever-wall pairs, assign them to same colorId value
        colorId = 0
        links = {}
        for lever, wall in self.mapping.items():
            links[lever] = colorId
            links[wall[1]] = colorId
            colorId += 1
        
        # print out maze
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                tile = self.grid[i][j]
                if tile == "P":
                    # player
                    output += formatColored(tile, "green")
                elif tile == "B":
                    # bot
                    output += formatColored(tile, "red")
                elif (i,j) in links:
                    # lever or wall
                    output += formatBg(tile, links[(i,j)])
                else:
                    output += tile
            output += "\n"
        print(output)

    # Output a path from start to goal in the maze (assuming both are empty spaces), else returns None
    def BFS(self, start, goal):
        visited = {}
        queue = []
        visited[start] = None
        queue.append(start) # what is the start node?
        while len(queue) > 0:
            node = queue[0]
            del queue[0]
            #print(node, self.graph[node])
            if node == goal:
                return createPath(start, goal, visited) # are we returning the path from start to end?
            else:
                if node not in self.graph:
                    self.getStringMaze()
                for new_node in self.graph[node]:
                    if new_node not in visited:
                        visited[new_node] = node
                        queue.append(new_node)
        return None
    
    # Returns if it's possible to go from currentPos to newPos
    def checkLegal(self, currentPos, newPos):
        if abs(currentPos[0] - newPos[0]) == 1 and currentPos[1] != newPos[1]:
            print("Illegal move: vertial bad movement")
            print(currentPos, newPos)
            return False # Can only move up down
        if abs(currentPos[1] - newPos[1]) == 1 and currentPos[0] != newPos[0]:
            print("Illegal move: horizontal bad movement")
            print(currentPos, newPos)
            return False # Can only move left right
        if abs(currentPos[1] - newPos[1]) > 1 or abs(currentPos[0] - newPos[0]) > 1:
            print("Illegal move: bad movement")
            print(currentPos, newPos)
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
    
    def countClosed(self):
        cnt = 0
        for i in self.mapping:
            cnt += (i[0] == 1)
        return cnt
    
    # Toggles the lever at leverPos.
    def toggleLever(self, leverPos):
        active, targetWall = self.mapping[leverPos]
        if targetWall == self.player or targetWall == self.bot:
            return
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

def formatColored(str, color):
    if color == "green":
        return "\033[92m{}\033[00m".format(str)
    if color == "red":
        return "\033[91m{}\033[00m".format(str)
    if color == "yellow":
        return "\033[93m{}\033[00m".format(str)
    if color == "blue":
        return "\033[94m{}\033[00m".format(str)
    if color == "magenta":
        return "\033[95m{}\033[00m".format(str)
        
def formatBg(str, colorId):
    id = colorId % 5
    if id == 0:
        # yellow
        return "\033[43m{}\033[00m".format(str)
    if id == 1:
        # blue
        return "\033[44m{}\033[00m".format(str)
    if id == 2:
        # magenta
        return "\033[45m{}\033[00m".format(str)
    if id == 3:
        # red
        return "\033[41m{}\033[00m".format(str)
    if id == 4:
        # green
        return "\033[42m{}\033[00m".format(str)