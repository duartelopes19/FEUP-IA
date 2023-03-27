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
        self.size = int(input("board size? "))
        self.board = Board(self.size)
        self.restore_mirror = False
        self.mode = input("difficulty? (easy/normal) ")

     # Define function to check if a ghost has won
    def check_win(self):
        if(self.mode=='easy'):
            if(len(self.players[0].ghostsReleased)==3):
                print('Player 1 Wins')
                return True

            elif(len(self.players[1].ghostsReleased)==3):
                print('Player 2 Wins')
                return True
            
            else:
                return False
        elif(self.mode =='normal'):
                if ('Red 1'in self.players[0].ghostsReleased  and 'Blue 1'  in self.players[0].ghostsReleased  and 'Yellow 1' in self.players[0].ghostsReleased ):
                   print('Player 1 Wins')
                   return True

                elif ('Red 2'in self.players[1].ghostsReleased  and 'Blue 2'  in self.players[1].ghostsReleased and 'Yellow 2' in self.players[1].ghostsReleased):
                    print('Player 2 Wins')
                    return True
                else:
                    return False
        
    
    def valid_moves(self, from_row, from_col, ghost):
        
        valid_moves= []


        #UP
        if(from_row - 1 >= 0):
            if(str(self.board.map[from_row-1][from_col])[:6]=='Mirror'):
                valid_moves.append('up mirror')
            elif((self.board.map[from_row-1][from_col]=='Red') or (self.board.map[from_row-1][from_col]=='Blue') or (self.board.map[from_row-1][from_col]== 'Yellow')):
                valid_moves.append('up')
            elif(str(self.board.map[from_row-1][from_col])[:6]!='Portal' and ghost.color!=self.board.map[from_row-1][from_col].color):
                valid_moves.append('up')
            

        #DOWN
        if(from_row + 1 < self.size):
            if(str(self.board.map[from_row+1][from_col])[:6]=='Mirror'):
                valid_moves.append('down mirror') 
            elif((self.board.map[from_row+1][from_col]=='Red') or (self.board.map[from_row+1][from_col]=='Blue') or (self.board.map[from_row+1][from_col]== 'Yellow')):
                valid_moves.append('down')
            elif(str(self.board.map[from_row+1][from_col])[:6]!='Portal' and ghost.color!=self.board.map[from_row+1][from_col].color):
                valid_moves.append('down')
        
        #LEFT
        if(from_col - 1 >= 0):
            if(str(self.board.map[from_row][from_col-1])[:6]=='Mirror'):
                valid_moves.append('left mirror')
            elif((self.board.map[from_row][from_col-1]=='Red') or (self.board.map[from_row][from_col-1]=='Blue') or (self.board.map[from_row][from_col-1]== 'Yellow')):
                valid_moves.append('left')
            elif(str(self.board.map[from_row][from_col-1])[:6]!='Portal' and ghost.color!=self.board.map[from_row][from_col-1].color):
                valid_moves.append('left')
            
        #RIGHT
        if(from_col + 1 < self.size):
            if(str(self.board.map[from_row][from_col+1])[:6]=='Mirror'):
                valid_moves.append('right mirror')
            elif((self.board.map[from_row][from_col+1]=='Red') or (self.board.map[from_row][from_col+1]=='Blue') or (self.board.map[from_row][from_col+1]== 'Yellow')):
                valid_moves.append('right')
            elif(str(self.board.map[from_row][from_col+1])[:6]!='Portal' and ghost.color!=self.board.map[from_row][from_col+1].color):
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

    if(action =='release'):
        for i in range(len(game.board.dungeon)):
            if(str(game.board.dungeon[i])[-1]==str(game.curr_player.number)):
                game.curr_player.add_ghost_to_dungeon(game.board.dungeon[i])
        
        if(len(game.curr_player.dungeon)==0):
            print('No Ghosts In the Dungeon')
            continue
        else: 
            for i in range(len(game.board.dungeon)):
                if(str(game.board.dungeon[i])[-1]==str(game.curr_player.number)):
                    print(game.board.dungeon[i], end="\n")
            print("\n")
            released = input('Which Ghost you want to release? ')

            for i in range(len(game.board.dungeon)):
                if(str(game.board.dungeon[i]) == released):
                    released = game.board.dungeon[i]
                    break

            if(game.board.release_dungeon(released,game.curr_player)):
                game.change_player()
            continue

    



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

        if(move[-6:] == 'mirror'):
            game.board.move_to_mirror(from_row, from_col, move)
            game.restore_mirror = True
            continue
        else:
            game.board.move_ghost(from_row ,from_col,move)    

        for i in range(len(valid_moves)):
            print(valid_moves[i])

        print("Dungeon: ")
        print("Player 1: ", end="")
        for i in range(len(game.board.dungeon)):
            if(str(game.board.dungeon[i])[-1]=='1'):
                print(game.board.dungeon[i], end=" ")
        print('\n')
        print("Player 2: ", end="")
        for i in range(len(game.board.dungeon)):
            if(str(game.board.dungeon[i])[-1]=='2'):
                print(game.board.dungeon[i], end=" ")
        print('\n')

        if(game.restore_mirror):
            game.board.restore_mirrors()
            game.restore_mirror = False
        
        game.board.portal_suction()
        for i in range(len(game.board.released)):
            if(str(game.board.released[i])[-1]=='2'):
                game.players[1].ghostsReleased.append(game.board.released[i])
            elif(str(game.board.released[i])[-1]=='1'):
                game.players[0].ghostsReleased.append(game.board.released[i])
        
        print('Player 1 released ghosts:', end = '\n')
        for i in range(len(game.players[0].ghostsReleased)):
            print(game.players[1].ghostsReleased[i], end='\n')
        
        print('Player 2 released ghosts:', end = '\n')
        for i in range(len(game.players[1].ghostsReleased)):
            print(game.players[1].ghostsReleased[i], end='\n')
    
    else:
        continue
    
    if(game.check_win()==True):
        break
        
   

    """  
    def update_board(self, move):
        # TODO: Implement the update of the board after each move
        
    def is_game_over(self):
        # TODO: Implement the check for game over

 """