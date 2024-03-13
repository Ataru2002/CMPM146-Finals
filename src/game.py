from gameMaze import gameMaze, BFS
import time

# Note: this is running from \src
test = gameMaze("../mazes/maze1.txt")

# print(test.getGrid())

# print(test.getString())

# print(BFS(test, test.start, test.lever))
# print(test.getBotPos())
# print(test.getPlayerPos())

isLeverActivated = False

while (True):
    print(test.getString())
    if (not isLeverActivated):
        botPath = BFS(test, test.getBotPos(), test.lever)
        diff = (botPath[1][0] - botPath[0][0], botPath[1][1] - botPath[0][1])
        print(diff)
        if diff == (1, 0):
            test.botAction('d')
        if diff == (-1, 0):
            test.botAction('u')
        if diff == (0, 1):
            test.botAction('r')
        if diff == (0, -1):
            test.botAction('l')
    
    if (test.getBotPos() == test.lever):
        isLeverActivated = True
    
    if (isLeverActivated):
        botPath = BFS(test, test.getBotPos(), test.end)
        diff = (botPath[1][0] - botPath[0][0], botPath[1][1] - botPath[0][1])
        print(diff)
        if diff == (1, 0):
            test.botAction('d')
        if diff == (-1, 0):
            test.botAction('u')
        if diff == (0, 1):
            test.botAction('r')
        if diff == (0, -1):
            test.botAction('l')
    
    if (test.getBotPos() == test.end):
        break

# while (True):
#     print(test.getString())
    # action = input("What is your next move? [u/d/l/r/q]: ").lower()
    # test.playerAction(action)
    