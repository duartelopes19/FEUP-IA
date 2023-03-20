from player import *
from ghost import *
from position import *
from board import *



size = input("board size?")
board = Board(size)
ROWS = size
COLS = size 
GHOST_TYPE= ['first','second']
GHOST_COLOR = ['Red', 'Blue', 'Yellow']

ACTIONS = ['Move', 'Fight', 'Release']


class Game:
    def __init__(self):
        self.dungeon = []
        self.players = [Player(1),Player(2)]
        self.curr_player = self.players[0]
        
        # Initialize the board with empty cells
        #self.board = 
        
        # Initialize the ghosts
        self.init_ghosts(self.players[0],"G1")
        self.init_ghosts(self.players[1],"G2")
        
    def init_ghosts(self, player, symbol):
        # TODO: Implement the initialization of the ghosts
        for i in range(3):
            player.add_ghost(Ghost(red,symbol))
            player.add_ghost(Ghost(yellow,symbol))
            player.add_ghost(Ghost(blue,symbol))

    
        
"""         
    def is_valid_move(self, move):
        # TODO: Implement the check for valid moves
        
    def update_board(self, move):
        # TODO: Implement the update of the board after each move
        
    def is_game_over(self):
        # TODO: Implement the check for game over

 """