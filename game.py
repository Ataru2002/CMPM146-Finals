from gameMaze import gameMaze

test = gameMaze("./maze1.txt")

#test.getGridMaze()

test.getStringMaze()

#print(test.BFS(test.start, test.lever))
test.getGraphMaze()
test.updatePos((13, 2), 0)
test.getGraphMaze()
test.getStringMaze()