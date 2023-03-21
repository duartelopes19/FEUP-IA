from player import *
from ghost import *
from position import *
from board import *



GHOST_TYPE= ['first','second']
GHOST_COLOR = ['Red', 'Blue', 'Yellow']

ACTIONS = ['Move', 'Fight', 'Release']


class Game:
    def __init__(self):
        self.players = [Player(1),Player(2)]
        self.curr_player = self.players[0]
        self.size = int(input("board size?"))
        self.board = Board(self.size)    

        
    def valid_moves(self, from_row, from_col, ghost):
        
        valid_moves= []

        #UP
        if(from_row - 1 >= 0):
            if(str(self.board.map[from_row-1][from_col])[:6]!='Portal' and ghost.color!=self.board.map[from_row-1][from_col].color):
                valid_moves.append('up')

        #DOWN
        if(from_row + 1 < self.size):
            if(str(self.board.map[from_row+1][from_col])[:6]!='Portal' and ghost.color!=self.board.map[from_row+1][from_col].color):
                valid_moves.append('down')
        
        #LEFT
        if(from_col - 1 >= 0):
            if(str(self.board.map[from_row][from_col-1])[:6]!='Portal' and ghost.color!=self.board.map[from_row][from_col-1].color):
                valid_moves.append('left')
            
        #RIGHT
        if(from_col + 1 < self.size):
            if(str(self.board.map[from_row][from_col+1])[:6]!='Portal' and ghost.color!=self.board.map[from_row][from_col+1].color):
                valid_moves.append('right')
        
        return valid_moves
    
    def change_player(self):
        if(self.curr_player.number == 1):
            self.curr_player = self.players[1]
        else:
            self.curr_player = self.players[0]




        
game = Game()

while(True):
    game.board.print_board()   
    print("\n"+str(game.curr_player))
    action = input('Enter action (move/release): ')

    if(action=='move'):
        from_row = int(input('Enter row of ghost to move (1-'+str(game.size)+'): ')) - 1
        from_col = int(input('Enter column of ghost to move (1-'+str(game.size)+'): ')) - 1
        
        ghost = game.board.map[from_row][from_col]

        if(type(ghost)==str or ghost.symbol != game.curr_player.number):
            print("That position is inaccessible!")
            continue
        
        valid_moves = game.valid_moves(from_row, from_col, ghost)

        print("These are the valid moves: ")
        for i in range(len(valid_moves)):
            print(valid_moves[i])
        
        move = input('Enter the move you want to perform : ')

        if(move not in valid_moves):
            print("That move is invalid, try again!")
            continue

        game.board.move_ghost(from_row ,from_col,move)    

        for i in range(len(valid_moves)):
            print(valid_moves[i])

        print("Dungeon: ", end="")
        for i in range(len(game.board.dungeon)):
            print(game.board.dungeon[i], end=" ")
        print('\n')
        
        game.change_player()

    else:
        break
    
        
   

    """  
    def update_board(self, move):
        # TODO: Implement the update of the board after each move
        
    def is_game_over(self):
        # TODO: Implement the check for game over

 """