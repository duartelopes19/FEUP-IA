from position import *
from math import *

COLORS = ['Red', 'Blue', 'Yellow']


class Board:

    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        #self.list[4][4] = 'Dungeon'
        self.dungeon = []
        # portals -> (color, col, row, orientation)
        self.portals = {('Red',ceil(size/2),0,'up'),('Blue',size,ceil(size/2),'right'),('Yellow',ceil(size/2),size,'down')}
    

        
        
        """ self.grid = [
            ['B','R','PR','B','R'],
            ['Y','M','Y','M','Y'],
            ['R','B','R','B','PY'],
            ['B','M','Y','M','R'],
            ['Y','R','PB','B','Y'],
        ]
 """
    def is_empty(self, row, col):
        return self.grid[row][col] is None
    
    def add_ghost(self, ghost, row, col):
        ghost.row = row
        ghost.col = col
        self.grid[row][col] = ghost

    def remove_ghost(self, row, col):
        ghost = self.grid[row][col]
        self.grid[row][col] = None
        return ghost
    
    def move_ghost(self, row1, col1, row2, col2):
        ghost = self.remove_ghost(row1, col1)
        self.add_ghost(ghost, row2, col2)

    def get_adjacent_chambers(self, row, col, size):
        adjacent_chambers = []
        if row > 0:
            adjacent_chambers.append((row-1, col))
        if row < size-1:
            adjacent_chambers.append((row+1, col))
        if col > 0:
            adjacent_chambers.append((row, col-1))
        if col < size-1:
            adjacent_chambers.append((row, col+1))
        return adjacent_chambers

    def get_mirror_chambers(self,size):
        mirror_chambers = []
        for row in range(size):
            for col in range(size):
                if (row, col) != (2, 2) and \
                   (row == 0 or row == size-1 or col == 0 or col == size-1):
                    mirror_chambers.append((row, col))
        return mirror_chambers








'''
    def drawBoard(self):
        print('-' * (self.size * 4 + 1))
        for row in self.grid:
            print('|', end='')
            for cell in row:
                if cell == 'B':
                    print(' B ', end='')
                if cell=='R':
                    print(' R ', end='')
                if cell=='PR':
                    print(' PR', end='')
                if cell=='Y':
                    print(' Y ', end='')
                if cell=='M':
                    print(' M ', end='')
                if cell=='PY':
                    print(' PY', end='')
                if cell=='PB':
                    print(' PB', end='')
                print('|', end='')
            print()
            print('-' * (self.size * 4 + 1))



    def is_valid_position(self, position):
        x, y = position
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def is_empty(self, position):
        x, y = position
        return self.grid[x][y] is None

    def get_ghost(self, position):
        x, y = position
        return self.grid[x][y]

    def move_ghost(self, source, target):
        x1, y1 = source
        x2, y2 = target
        ghost = self.grid[x1][y1]
        self.grid[x1][y1] = None
        self.grid[x2][y2] = ghost
        ghost.position = target

    def __str__(self):
        result = ""
        for i in range(self.size):
            for j in range(self.size):
                ghost = self.grid[j][i]
                if ghost is None:
                    result += "."
                elif ghost.color == "white":
                    result += "W"
                else:
                    result += "B"
            result += "\n"
        return result
    
board = Board()
board.drawBoard()'''
