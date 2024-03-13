# a class that stores the following:
# 2D array representation x
# string array that stores the entire maze x
# a function that prints out the entire maze when called x
# graph representation of the maze x
# states (Where the player is right now, where the bot is right now)
# states that can't be mutate (i.e where the levers, openable walls, start points, end points, etc)
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
                        if self.grid[i][j] == 'S':
                            self.start = (i, j)
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
        print(self.graph)

    def getGridMaze(self):
        print(self.grid)

    def getStringMaze(self):
        output = ""
        for instances in self.grid:
            for j in instances:
                output += j
            output += "\n"
        print(output)

def BFS(gameMaze, start, goal):
    visited = {}

    queue = []
    visited[start] = None
    queue.append(start) # what is the start node?
    while queue:
        node = queue.pop()
        print(node)
        if node == goal:
            print("finding path now")
            return createPath(start,goal,visited) # are we returning the path from start to end?
        else:
            for new_node in gameMaze.graph[node]:
                if new_node not in visited:
                    visited[new_node] = node
                    queue.append(new_node)
                
                

    pass

def createPath(start,goal,visited):
    path = [goal]
    current = goal
    while(current != start):
        #print(current)
        path.append(visited[current])
        current = visited[current]
        
    return path
        
