########################################################################
# Zhili Wang                                                           #
# CS5001 Homework 6                                                    #
# maze.py                                                              #
#                                                                      # 
# * a Maze class that constructs a maze object by inputting a txt file #
#   along with its encapsulated method/operations                      #
########################################################################
class Maze:
    def __init__(self, fname):
    ########################################################################
    # Parameter(s):                                                        #
    # - self                                                               # 
    # - fname: txt file name or route                                      #
    # Return: none                                                         #
    # Purpose: constructor of the class                                    #
    ########################################################################
        self.read_maze_file(fname)
        
    def read_maze_file(self, fname):
    ########################################################################
    # Parameter(s):                                                        #
    # - self                                                               # 
    # - fname: txt file name or route                                      #
    # Return: none                                                         #
    # Purpose: defines attributes of the Maze object                       #
    ########################################################################
        try:
            fd = open(fname, "r")
            linenum = 1
            vals = [int(x) for x in fd.readline().split()]
            self.dims = (vals[0], vals[1])
            self.start = (vals[2], vals[3])
            self.end = (vals[4], vals[5])
            linenum += 1
            fd.readline()    # discard top wall
            self.right_walls = []
            self.bottom_walls = []
            for r in range(self.dims[0]):
                # process side walls
                self.right_walls.append([])
                linenum += 1
                s = fd.readline()[2::2]
                for c in range(self.dims[1]):
                    self.right_walls[r].append(s[c] == '|')
                # process bottom walls
                self.bottom_walls.append([])
                linenum += 1
                s = fd.readline()[1::2]
                for c in range(self.dims[1]):
                    self.bottom_walls[r].append(s[c] == '-')
        except FileNotFoundError as err:
            raise  # re-raise exception
        except Exception as err:
            print("Processing line", linunum, "raised exception:", err)
            raise  # re-raise exception

    def getSize(self):
    ########################################################################
    # Parameter(s):                                                        #
    # - self                                                               # 
    # Return: self.dims                                                    #
    # Purpose: accessor that gets maze object's dimensions (col & row)     #
    ########################################################################
        return self.dims
    
    def getStart(self):
    ########################################################################
    # Parameter(s):                                                        #
    # - self                                                               # 
    # Return: self.start                                                   #
    # Purpose: daccessor that gets maze object's starting coordinates      #
    ########################################################################
        return self.start
    
    def getEnd(self):
    ########################################################################
    # Parameter(s):                                                        #
    # - self                                                               # 
    # Return: self.end                                                     #
    # Purpose: daccessor that gets maze object's destination coordinates   #
    ########################################################################
        return self.end

    def openDirs(self, row_col_pair):
    ########################################################################
    # Parameter(s):                                                        #
    # - self                                                               #
    # - row_col_pair: a tuple with a pair of coordinate (inside the maze)  #
    # Return: a list of available directions (strings)                     #
    # Purpose: show directions that one can go if it's in a square of the  #
    #           maze                                                       #
    ########################################################################
        direc = ["D","R","U","L"]
        # if coordinates are negative or out of dimension ranges
        if (row_col_pair[0] < 0 or row_col_pair[1] < 0 or \
            self.dims[0] < row_col_pair[0] or \
            self.dims[1] < row_col_pair[1]):
            return "Invalid coordinates."
        # (R, C)'s Down / Bottom
        else:
            if self.bottom_walls[row_col_pair[0]][row_col_pair[1]]:
                direc.remove("D")
            # (R, C)'s Right
            if self.right_walls[row_col_pair[0]][row_col_pair[1]]:
                direc.remove("R")
            # (R, C)'s Upper
            # upper walled & premier
            if row_col_pair[0] - 1 < 0:
                direc.remove("U")
            # upper walled but not premier
            elif self.bottom_walls[row_col_pair[0] - 1][row_col_pair[1]]:
                direc.remove("U")
            # (R, C)'s Left = (R, C-1)'s Right
            # left walled & premier
            if row_col_pair[1] - 1 < 0:   
                direc.remove("L")
            # left walled but not premier
            elif self.right_walls[row_col_pair[0]][row_col_pair[1] - 1]:
                direc.remove("L")
        return direc
        

