# a class that stores the following:
# 2D array representation x
# string array that stores the entire maze x
# a function that prints out the entire maze when called x
# graph representation of the maze
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
        except FileNotFoundError:
            print(f"File not found: {filename}")
    
    def getGridMaze(self):
        print(self.grid)
    
    def getStringMaze(self):
        output = ""
        for instances in self.grid:
            for j in instances:
                output += j
            output += "\n"
        print(output)