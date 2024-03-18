'''
Purpose: This file will be use as a game console where players input their input from the controls, bot making moves, until the game ended
Current task:
- Get the input from a human (p1)
- Get the input from a bot (p2)
- Get a while loop to continously get input, update state, until the game state is terminal
'''

from gameMaze import gameMaze, formatColored
import mctsBot
import constants
import sys
import random
import copy


maze = None
input_maze = None
if len(sys.argv)>1:
    input_maze = sys.argv[1]

if input_maze:
    maze = gameMaze(input_maze)
else:
    print("USAGE: python game.py <maze_file>")
    print("Resorting to default...")
    maze = gameMaze("./mazes/default_maze.txt")

maze.getStringMaze()
previous = []
while True:
    
    print(formatColored("-----------------------BOT TURN-----------------------", "red"))
    maze.getStringMaze()
    chosen = mctsBot.think(maze, maze.getPosBot(), previous)
    maze.updatePos(chosen, constants.USER_BOT)
    if(maze.isTerminal()):
        break
    
    print(formatColored("-----------------------PLAYER TURN-----------------------", "green"))
    maze.getStringMaze()
    while True:
        move = input("(U)p, (D)own, (L)eft, (R)ight, (Q)uit: ").lower()
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
            print("Quitting game...")
            quit()
        else:
            print("ERROR: Invalid input.")
            continue
        if maze.checkLegal(maze.player, destination):
            break
    maze.updatePos(destination, constants.USER_PLAYER)
    if(maze.isTerminal()):
        break

if maze.winner() == constants.USER_BOT:
    print(formatColored("You lost. L + Ratio", "red"))
else:
    print(formatColored("You won!", "green"))


