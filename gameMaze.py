# a class that stores the following:
# 2D array representation x
# string array that stores the entire maze x
# a function that prints out the entire maze when called x
# graph representation of the maze x
# states (Where the player is right now, where the bot is right now) x
# states that can't be mutate (i.e where the levers, openable walls, start points, end points, etc) x
class gameMaze:
    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                self.grid = []
                current = []
                for i in content:
                    if i != '\n':
                        current.append(i)
                    if i == '\n':
                        self.grid.append(current)
                        current = []

                for i in range(0,len(self.grid)):
                    for j in range(0,len(self.grid)):
                        if self.grid[i][j] == 'P':
                            self.player = (i, j)
                        if self.grid[i][j] == 'B':
                            self.bot = (i, j)
                        if self.grid[i][j] == 'E':
                            self.end = (i, j)
                        if self.grid[i][j] == 'L':
                            self.lever = (i, j)
                        if self.grid[i][j] == 'A':
                            self.openWall = (i, j)

        except FileNotFoundError:
            print(f"File not found: {filename}")

        self.graph = {}
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] != '#':
                    self.graph[(i, j)] = []
                    if i > 0 and self.grid[i - 1][j] != '#': self.graph[(i, j)].append((i - 1, j))
                    if i < len(self.grid) - 1 and self.grid[i + 1][j] != '#': self.graph[(i, j)].append((i + 1, j))
                    if j > 0 and self.grid[i][j - 1] != '#': self.graph[(i, j)].append((i, j - 1))
                    if j < len(self.grid) - 1 and self.grid[i][j + 1] != '#': self.graph[(i, j)].append((i, j + 1))

    def getGridMaze(self):
        print(self.grid)

    def getStringMaze(self):
        output = ""
        for instances in self.grid:
            for j in instances:
                output += j
            output += "\n"
        print(output)

    
    # Output a path from a point to any other point in the maze (assuming both are empty spaces)
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
    
    def checkLegal(self, currentPos, newPos):
        print(currentPos, newPos)
        if abs(currentPos[0] - newPos[0]) == 1 and currentPos[1] != newPos[1]:
            print("wrong movement")
            return False # Can only move up down
        if abs(currentPos[1] - newPos[1]) == 1 and currentPos[0] != newPos[0]:
            print("wrong movement")
            return False # Can only move left right
        if abs(currentPos[1] - newPos[1]) > 1 or abs(currentPos[0] - newPos[0]) > 1:
            print("wrong movement")
            return False # Moves too far
        if self.grid[newPos[0]][newPos[1]] == '#':
            print("wall")
            return False # Can only move in empty spaces, not walls
        return True

    def updatePlayer(self, newPos):
        oldPos = (self.player[0], self.player[1])
        if not self.checkLegal(oldPos, newPos):
            return False
        self.grid[oldPos[0]][oldPos[1]] = ' '
        self.grid[newPos[0]][newPos[1]] = 'P'
        return True

    def updateBot(self, newPos):
        oldPos = (self.bot[0], self.bot[1])
        if not self.checkLegal(oldPos, newPos):
            return False
        self.grid[oldPos[0]][oldPos[1]] = ' '
        self.grid[newPos[0]][newPos[1]] = 'B'
        return True
        
def createPath(start, goal, visited):
        path = [goal]
        current = goal
        while(current != start):
            path.append(visited[current])
            current = visited[current]
        path.reverse()
        return path