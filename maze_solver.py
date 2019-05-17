########################################################################
# Zhili Wang                                                           #
# CS5001 Homework 6                                                    #
# maze_solver.py                                                       #
# * a user interface to implement the Maze class                       #
########################################################################
from maze import *

def can_go(dirs, coors, track_ls):
########################################################################
# Parameter(s):                                                        #
# - dirs: a list of strings (returned from openDirs)                   #
# - coors: a tuple of valid coordinates inside of maze object          #
# - track_ls: a list of tuples of visited rooms/squares of maze obj    #
# Return:                                                              #
# <class 'list'> a list of tuples                                      #
# Purpose:                                                             #
#           - turning the list returned from openDirs, compares a list #
#           of tracked list of visited rooms, and outputs a list that  #
#           we "can go" to from our CURRENT position                   #
#           - make outcome of openDirs easier to compare with "track"  #                                                
# Example: it first turns ['D', 'R'] and (1, 1)) to a list of          #
#          [(2, 1), (1, 2)]. Then compare it with [(1, 2), (1, 3)],    #
#          and we get [(2, 1)]                                         #
# Note: since I used set(), this function only takes out the           #
#       intersected tuples between the two lists                       #
########################################################################
    # dirs_ls is list of ALL rooms we "can go" to according to openDirs
    dirs_ls = []
    if 'D' in dirs:
        dirs_ls.append((coors[0] + 1, coors[1]))
    if 'R' in dirs:
        dirs_ls.append((coors[0], coors[1] + 1))
    if 'U' in dirs:
        dirs_ls.append((coors[0] - 1, coors[1]))
    if 'L' in dirs:
        dirs_ls.append((coors[0], coors[1] - 1))
    # now compare it to "track" list and remove visited rooms
    return list(set(dirs_ls) - set(track_ls))

def solve_maze(maze, pos, end, track, path):
########################################################################
# Parameter(s):                                                        #
# - maze: an obj created from Maze class                               #
# - pos: our current position coordinate in a tuple                    #
# - end: our destination postion coordinate in a tuple                 #
# - track: a list of coordinates indicating all visited rooms          #
# - path: a list of coordinates of adjacant rooms indicating a valid   #
#         path from starting position to destination                   #
# Return:                                                              #
# <class 'list'> path: a list of coordinates of adjacant rooms         #
#                indicating a valid                                    #
#         path from starting position to destination                   #
# Purpose: given maze object's attributes as information, with help    #
#          from a tracking list, to find a valid path implementing     #
#          Depth-First-Search with recursive backtracking              #
########################################################################
    # base case:
    if pos == end:# and pos not in path:
        path.append(pos)
        return path

    else:
        # when we are not at destination and recursion is called,
        # add current position to both track and path
        if pos not in track and pos not in path:
            track.append(pos)
            path.append(pos)
        # get a list of rooms we can go, taking out visited room in "track"
        open_dirs = can_go(maze.openDirs(pos), pos, track)
        # keeps going (dfs) as long as we have an available room to go
        if len(open_dirs) > 0:
            # down/bottom neighbor
            if (pos[0] + 1, pos[1]) in open_dirs:
                pos = (pos[0] + 1, pos[1])
            # right neighbor
            elif (pos[0], pos[1] + 1) in open_dirs:
                pos = (pos[0], pos[1] + 1)
            # upper neighbor
            elif (pos[0] - 1, pos[1]) in open_dirs:
                pos = (pos[0] - 1, pos[1])
            # left neighbor
            elif (pos[0], pos[1] - 1) in open_dirs:
                pos = (pos[0], pos[1] - 1)
            solve_maze(maze, pos, end, track, path)
        # backtracking when hit a deadend (no room to go from current position)
        else:
            # remove last room in path,
            # use last element as new CURRENT position --> perform recursion
            # if maze backtrack to starting room and no where to go: unsolvable
            del(path[-1])
            if len(path) > 0:
                pos = path[-1]
                solve_maze(maze, pos, end, track, path)
    return path

def main():
########################################################################
# Parameter(s):                                                        #
# maze: a Maze object initialized with a user-defined TXT file         #
# file_name: TXT file name                                             #
# Return: none                                                         #
# Purpose: creating a Maze object, define variables and call function  #    
########################################################################
    is_again = "y"
    while is_again == "y":
        f_name = input("Please input your txt-format maze file name: ")
        # check if file name ends with "txt" to ensure TXT format
        while f_name.split(".")[-1] != ("txt"):
            f_name = input('TXT file only, please make sure to include ".txt": ')
        try:    
            maze = Maze(f_name)
        except FileNotFoundError as err:
            print("File not found or error with maze file:", err)
        except Exception as err:
            print("Unexpected exception:", err)

        # initializing variables
        maze = Maze(f_name)
        pos = maze.getStart()
        end = maze.getEnd()
        track = []
        path = []

        # maze unsolvable
        if len(solve_maze(maze, pos, end, track, path)) == 0:
            print("The maze created from " + f_name + " is unsolvable!")
        # solvable
        else:
            print("The maze created from " + f_name + " has the following path:")
            print(solve_maze(maze, pos, end, track, path))
            
        is_again = input("\nWould you like to test another file (Y/N)? ").lower()
main()

