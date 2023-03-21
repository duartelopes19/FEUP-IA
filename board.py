from position import *
from math import *
##from game import *
from ghost import *
from player import *
import random 
import pygame
from pygame import *

COLORS = ['Red', 'Blue', 'Yellow']


class Board:

    def __init__(self, size):
        self.size = size
        self.grid = [["" for _ in range(size)] for _ in range(size)]
        self.map = [["" for _ in range(size)] for _ in range(size)]
        self.populate()
        #self.players = [Player(1), Player(2)]
        #self.give_ghosts()

        #self.list[4][4] = 'Dungeon'

        # portals -> (color, orientation)
        self.portals = {('Portal Red','up'),('Portal Blue','down'),('Portal Yellow','right')}
    
    def is_empty(self, row, col):
        return self.grid[row][col] is None
    '''
    def give_ghosts(self):
        for player in self.players:
            for i in range(0, 3):
                player.add_ghost(Ghost(COLORS[i]))
    
    def place_ghosts2(self):
        for row in range(self.size):
            for col in range(self.size):


    '''


    def add_ghost(self, ghost, row, col):
        ghost.row = row
        ghost.col = col
        self.map[row][col] = ghost

    def remove_ghost(self, row, col):
        ghost = self.map[row][col]
        self.map[row][col] = ""
        return ghost

    def fight(self, ghost, row, col):

        '''Red ghosts beat blue ones.
        Blue ghosts beat yellow ones
        Yellow ghosts beat red ones'''

        color = ghost.color        
        ghost2 = self.map[row][col]
        color2 = ghost2.color

        if(color=='Red'):
            if(color2 == 'Blue'):
                return True
            else:
                return False
            
        elif(color == 'Blue'):
            if(color2 == 'Yellow'):
                return True
            else:
                return False
        
        elif(color == 'Yellow'):
            if(color2=='Red'):
                return True
            else:
                return False
                
        
    def send_to_dungeon(self,ghost,curr_player):
        curr_player.add_ghost_to_dungeon(ghost)
        
        
    def move_to_mirror(self, row, col, move):
        dir = move[:-7]

        ghost = self.remove_ghost(row, col)

        valid_mirrors = ['Mirror 1', 'Mirror 2', 'Mirror 3', 'Mirror 4']

        if(dir=='up'):
            valid_mirrors.remove(self.map[row-1][col])
        elif(dir=='down'):
            valid_mirrors.remove(self.map[row+1][col])
        elif(dir=='left'):
            valid_mirrors.remove(self.map[row][col-1])
        elif(dir=='right'):
            valid_mirrors.remove(self.map[row][col+1])
        
        
        print("These are the valid mirrors: ")
        for i in range(len(valid_mirrors)):
            print(valid_mirrors[i])
            

        i = input("Enter the mirror you want to move to (num): ")
        mirror = "Mirror " + str(i)

        (mrow, mcol) = self.positions[mirror]

        self.add_ghost(ghost, mrow, mcol)

        return

        
            
        
    def move_ghost(self, row, col, move, curr_player):
        
        ghost = self.remove_ghost(row, col)
        
        if(move == 'up'):
            if(self.fight(ghost, row-1, col)):
                self.send_to_dungeon(self.map[row-1][col], curr_player)
                self.add_ghost(ghost, row-1, col)
            else:
                self.send_to_dungeon(ghost,curr_player)
            
        elif(move == 'down'):
            if(self.fight(ghost, row+1, col)):
                self.send_to_dungeon(self.map[row+1][col], curr_player)
                self.add_ghost(ghost, row+1, col)
            else:
                self.send_to_dungeon(ghost,curr_player)

        elif(move == 'left'):
            if(self.fight(ghost, row, col-1)):
                self.send_to_dungeon(self.map[row][col-1], curr_player)
                self.add_ghost(ghost, row, col-1)
            else:
                self.send_to_dungeon(ghost,curr_player)

        elif(move == 'right'):
            if(self.fight(ghost, row, col+1)):
                self.send_to_dungeon(self.map[row][col+1], curr_player)
                self.add_ghost(ghost, row, col+1)
            else:
                self.send_to_dungeon(ghost,curr_player)
        
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

    def restore_mirrors(self):
        self.map[self.size - ceil(self.size/4)][floor(self.size/4)] = 'Mirror 3'
        self.map[self.size - ceil(self.size/4)][floor(self.size/2)+floor(self.size/4)] = 'Mirror 4'
        self.map[floor(self.size/4)][floor(self.size/4)] = 'Mirror 1'
        self.map[floor(self.size/4)][floor(self.size/2)+floor(self.size/4)] = 'Mirror 2'

    def print_board(self):
        """
        Print the game board.
        """
        print('----' * self.size)
        for row in range(self.size):
            print(str(row+1)+' |', end='')
            for col in range(self.size):
                print(' ' + str(self.map[row][col]) + ' |', end='')
            print('')
            print('-----' * self.size*2)
        for num in range(self.size):
            if(num==0): print('   '+str(num+1)+' | ', end='')
            else:
                print(str(num+1)+' | ', end='')

        """ print('----' * self.size)
        for row in range(self.size):
            print(str(row+1)+' |', end='')
            for col in range(self.size):
                print(' ' + self.grid[row][col] + ' |', end='')
            print('')
            print('----' * self.size)
        for num in range(self.size):
            if(num==0): print('   '+str(num+1)+' | ', end='')
            else:
                print(str(num+1)+' | ', end='') """


    def populate(self):

        # self.portals = {('Red',ceil(size/2),0,'up'),('Blue',size,ceil(size/2),'right'),('Yellow',ceil(size/2),size,'down')}

        self.grid[0][floor(self.size/2)] = 'Portal Red'
        self.grid[self.size - 1][floor(self.size/2)] = 'Portal Blue'
        self.grid[floor(self.size/2)][self.size-1] = 'Portal Yellow'
        
        self.grid[self.size - ceil(self.size/4)][floor(self.size/4)] = 'Mirror 3'
        self.grid[self.size - ceil(self.size/4)][floor(self.size/2)+floor(self.size/4)] = 'Mirror 4'
        self.grid[floor(self.size/4)][floor(self.size/4)] = 'Mirror 1'
        self.grid[floor(self.size/4)][floor(self.size/2)+floor(self.size/4)] = 'Mirror 2'

        self.map[0][floor(self.size/2)] = 'Portal Red'
        self.map[self.size - 1][floor(self.size/2)] = 'Portal Blue'
        self.map[floor(self.size/2)][self.size-1] = 'Portal Yellow'
        
        self.map[self.size - ceil(self.size/4)][floor(self.size/4)] = 'Mirror 3'
        self.map[self.size - ceil(self.size/4)][floor(self.size/2)+floor(self.size/4)] = 'Mirror 4'
        self.map[floor(self.size/4)][floor(self.size/4)] = 'Mirror 1'
        self.map[floor(self.size/4)][floor(self.size/2)+floor(self.size/4)] = 'Mirror 2'

        self.positions = {}
        for row in range(self.size):
            for col in range(self.size):
                value = self.grid[row][col]
                if value in ('Portal Red', 'Portal Blue', 'Portal Yellow', 'Mirror 1', 'Mirror 2', 'Mirror 3', 'Mirror 4'):
                    self.positions[value] = (row, col)
    

        for color in COLORS:
            for player in (1, 2):
                for _ in range(3):
                    row = random.randint(0, self.size-1)
                    col = random.randint(0, self.size-1)
                    while (self.map[row][col] != ""):
                        row = random.randint(0, self.size-1)
                        col = random.randint(0, self.size-1)
                    pos = Position(row, col)
                    ghost2 = Ghost(color, player, pos)
                    self.map[row][col] = ghost2
                    self.grid[row][col]= color
                                            
        


    """ def place_ghosts(self):
        for row in range(self.size):
            for col in range(self.size):
                if (self.grid[row][col]!='Portal Red' and self.grid[row][col]!='Portal Blue' and self.grid[row][col]!='Portal Yellow' and self.grid[row][col]!='Mirror'):
                    if('Red') self.ghosts[row][col] = Ghost(self.grid[row][col],random.randint(0,1),Position(row,col))
                
 """


""" # Initialize Pygame
pygame.init()

# Set up the game window
window_width = 640
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Ghost Adventure Board")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MIRROR = (127, 127, 127)

# Set up the board
board_size = board.size
cell_size = 64
board_width = cell_size * board_size
board_height = cell_size * board_size
board_left = (window_width - board_width) / 2
board_top = (window_height - board_height) / 2

pacman_angle_rad = math.radians(60)
window.fill(WHITE)
# Draw the board
for row in range(board_size):
    for col in range(board_size):
        cell_left = board_left + col * cell_size
        cell_top = board_top + row * cell_size
        cell_rect = pygame.Rect(cell_left, cell_top, cell_size, cell_size)
        pygame.draw.rect(window, WHITE, cell_rect, 2)

        cell_contents = board.grid[row][col]
        if cell_contents == "Portal Red":
            pygame.draw.circle(window, RED, cell_rect.center,cell_size//2)
            pygame.draw.circle(window, BLACK, cell_rect.center, cell_size // 2, 1)
            pygame.draw.arc(window, (0, 0, 0), pygame.Rect(cell_rect.center, pygame.math.degrees(pacman_angle_rad/2), math.degrees(-pacman_angle_rad/2), 0))
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        elif cell_contents == "Portal Blue":
            pygame.draw.arc(window, RED, cell_rect, 10, 20, 1)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        elif cell_contents == "Portal Yellow":
            pygame.draw.rect(window, YELLOW, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        elif cell_contents == "Mirror":
            pygame.draw.rect(window, MIRROR, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        elif cell_contents == "Blue":
            pygame.draw.rect(window, BLUE, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        elif cell_contents == "Red":
            pygame.draw.rect(window, RED, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        elif cell_contents == "Yellow":
            pygame.draw.rect(window, YELLOW, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
        else:
            pygame.draw.rect(window, GREEN, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)

# Update the display
pygame.display.update()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit() """




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
