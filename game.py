'''
Purpose: This file will be use as a game console where players input their input from the controls, bot making moves, until the game ended
Current task:
- Get the input from a human (p1)
- Get the input from a bot (p2)
- Get a while loop to continously get input, update state, until the game state is terminal
'''

from gameMaze import gameMaze
import constants
import sys
import random



maze = None
input_maze = None
if len(sys.argv)>1:
    input_maze = sys.argv[1]

if input_maze:
    maze = gameMaze(input_maze)
else:
    print("Usage: python game.py <maze_file>")
    print("default to maze1")
    maze = gameMaze("./mazes/maze1.txt")

maze.getStringMaze()
while(not maze.isTerminal()):
    
    print("-----------------------BOT TURN-----------------------")
    maze.getStringMaze()
    maze.updatePos(random.choice(maze.getLegalActions(maze.bot)), constants.USER_BOT)
    
    print("-----------------------PLAYER TURN-----------------------")
    maze.getStringMaze()
    while True:
        move = input("Your turn [ (U)p, (D)own, (L)eft, (R)ight, (Q)uit ]: ").lower()
        destination = None
        if move == "u":
            destination = (maze.player[0] - 1, maze.player[1])
        elif move == "d":
            destination = (maze.player[0] + 1, maze.player[1])
        elif move == "l":
            destination = (maze.player[0], maze.player[1] - 1)
        elif move == "r":
            destination = (maze.player[0], maze.player[1] + 1)
        elif move == "q":
            print("bye nerd 😘")
            quit()
        else:
            print("ERROR: PLAYER CANT READ!!!!! 🤣🤣🤣🤣")
            continue
        if maze.checkLegal(maze.player, destination):
            break
    maze.updatePos(destination, constants.USER_PLAYER)

print(f"Player {maze.winner()} won POGGERS 🤣😂😁😀😂🤗🤩😘😮😴🤗🥱😑!")


