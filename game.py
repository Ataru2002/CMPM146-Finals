from gameMaze import gameMaze, BFS

test = gameMaze("./maze1.txt")

test.getGridMaze()

test.getStringMaze()

print(BFS(test, test.start, test.lever))