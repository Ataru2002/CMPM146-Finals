# a class that stores the following:
# 2D array representation x
# string array that stores the entire maze x
# a function that prints out the entire maze when called x
# graph representation of the maze x
# states (Where the player is right now, where the bot is right now)
# states that can't be mutate (i.e where the levers, openable walls, start points, end points, etc)
import tiles

class gameMaze:
    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                self.grid = []
                current = []
                
                # initialize grid
                for i in content:
                    if i != '\n':
                        current.append(i)
                    if i == '\n':
                        self.grid.append(current)
                        current = []

                # find important tiles
                for i in range(0,len(self.grid)):
                    for j in range(0,len(self.grid)):
                        if self.grid[i][j] == tiles.BOT:
                            self.start = (i, j)
                        if self.grid[i][j] == tiles.END:
                            self.end = (i, j)
                        if self.grid[i][j] == tiles.LEVER:
                            self.lever = (i, j)
                        if self.grid[i][j] == tiles.OPENABLE_WALL:
                            self.openWall = (i, j)

        except FileNotFoundError:
            print(f"File not found: {filename}")
            quit()

        # initialize graph representation of maze (as a dictionary of paths)
        self.graph = {}
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] == tiles.WALL:
                    continue
                
                self.graph[(i, j)] = []
                
                # add adjacent tiles to current tile if not a wall
                if i > 0 and self.grid[i - 1][j] != tiles.WALL:
                    self.graph[(i, j)].append((i - 1, j))
                if i < len(self.grid) - 1 and self.grid[i + 1][j] != tiles.WALL:
                    self.graph[(i, j)].append((i + 1, j))
                if j > 0 and self.grid[i][j - 1] != tiles.WALL:
                    self.graph[(i, j)].append((i, j - 1))
                if j < len(self.grid) - 1 and self.grid[i][j + 1] != tiles.WALL:
                    self.graph[(i, j)].append((i, j + 1))
        # print(self.graph)

    def getGrid(self):
        return self.grid

    def getString(self):
        output = ""
        for instances in self.grid:
            for j in instances:
                output += j
            output += "\n"
        return output
    
    def getPlayerPos(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] == tiles.PLAYER:
                    return (i, j)
    
    def getBotPos(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] == tiles.BOT:
                    return (i, j)
    
    def playerAction(self, action):
        playerY, playerX = self.getPlayerPos()
        if action == 'q':
            print("Quitting game...")
            quit()
        if action == 'r':
            if (playerY, playerX + 1) in self.graph[(playerY, playerX)]:
                self.grid[playerY][playerX] = tiles.PATH
                self.grid[playerY][playerX + 1] = tiles.PLAYER
                print(f"Player moving to {(playerY, playerX + 1)}")
                return True
        if action == 'l':
            if (playerY, playerX - 1) in self.graph[(playerY, playerX)]:
                self.grid[playerY][playerX] = tiles.PATH
                self.grid[playerY][playerX - 1] = tiles.PLAYER
                print(f"Player moving to {(playerY, playerX - 1)}")
                return True
        if action == 'u':
            if (playerY - 1, playerX) in self.graph[(playerY, playerX)]:
                self.grid[playerY][playerX] = tiles.PATH
                self.grid[playerY - 1][playerX] = tiles.PLAYER
                print(f"Player moving to {(playerY - 1, playerX)}")
                return True
        if action == 'd':
            if (playerY + 1, playerX) in self.graph[(playerY, playerX)]:
                self.grid[playerY][playerX] = tiles.PATH
                self.grid[playerY + 1][playerX] = tiles.PLAYER
                print(f"Player moving to {(playerY + 1, playerX)}")
                return True
        print("ERROR: Player move is not possible.")
        return False
    
    def botAction(self, action):
        botY, botX = self.getBotPos()
        if action == 'r':
            if (botY, botX + 1) in self.graph[(botY, botX)]:
                self.grid[botY][botX] = tiles.PATH
                self.grid[botY][botX + 1] = tiles.BOT
                print(f"bot moving to {(botY, botX + 1)}")
                return True
        if action == 'l':
            if (botY, botX - 1) in self.graph[(botY, botX)]:
                self.grid[botY][botX] = tiles.PATH
                self.grid[botY][botX - 1] = tiles.BOT
                print(f"bot moving to {(botY, botX - 1)}")
                return True
        if action == 'u':
            if (botY - 1, botX) in self.graph[(botY, botX)]:
                self.grid[botY][botX] = tiles.PATH
                self.grid[botY - 1][botX] = tiles.BOT
                print(f"bot moving to {(botY - 1, botX)}")
                return True
        if action == 'd':
            if (botY + 1, botX) in self.graph[(botY, botX)]:
                self.grid[botY][botX] = tiles.PATH
                self.grid[botY + 1][botX] = tiles.BOT
                print(f"bot moving to {(botY + 1, botX)}")
                return True
        print("ERROR: Bot move is not possible.")
        return False
        
            
                

def BFS(gameMaze, start, goal):
    visited = {}

    queue = []
    visited[start] = None
    queue.append(start) # what is the start node?
    while queue:
        node = queue.pop()
        # print(node)
        if node == goal:
            print("finding path now")
            return createPath(start,goal,visited) # are we returning the path from start to end?
        else:
            for new_node in gameMaze.graph[node]:
                if new_node not in visited:
                    visited[new_node] = node
                    queue.append(new_node)
    # if goal was not found
    print("ERROR: Path not found")
    return None

def createPath(start, goal, visited):
    path = [goal]
    current = goal
    while(current != start):
        # print(current)
        path.append(visited[current])
        current = visited[current]
    path.reverse()
    return path
