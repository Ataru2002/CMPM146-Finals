from gameMaze import gameMaze

test = gameMaze("./maze1.txt")

#test.getGridMaze()

test.getStringMaze()

#print(test.BFS(test.start, test.lever))

test.updateBot((12, 1))


test.getStringMaze()