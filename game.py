from player import *
from ghost import *
from position import *
from board import *
import sys
import random



GHOST_TYPE= ['first','second']
GHOST_COLOR = ['Red', 'Blue', 'Yellow']

ACTIONS = ['Move', 'Fight', 'Release']
minimax_moves = []

""" 
if __name__ == '__main__':

    gameMode = -1
    while (True):
        print("\tMenu")
        print("0 - Exit")
        print("1 - Player vs Player")
        print("2 - Player vs AI Minimax")
        print("3 - AI Minimax vs AI Minimax")

        gameMode = int(input("Option: "))

        if(gameMode < 0 or gameMode > 4):
            print("\nInvalid option\nTry again\n")
            continue
        if(gameMode == 0): 
            sys.exit(0)
        if(gameMode == 1): 
            Game() """


class Game:
    def __init__(self):
        self.players = [Player(1),Player(2)]
        self.curr_player = self.players[0]
        self.size = 5
        self.board = Board(self.size)
        self.temp_board = Board(self.size)
        self.restore_mirror = False
        self.mode = input("difficulty? (easy/normal) ")

     # Define function to check if a ghost has won
    def check_win(self):
        if(self.mode=='easy'):
            if(len(self.players[0].ghostsReleased)==3):
                self.board.print_board()   
                print('Player 1 Wins')
                print("\n")
                return True

            elif(len(self.players[1].ghostsReleased)==3):
                self.board.print_board()   
                print('Player 2 Wins')
                print("\n")
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

        if(type(ghost)==str):
            return

        #UP
        if(from_row - 1 >= 0):
            if(str(self.board.map[from_row-1][from_col])[:6]=='Mirror'):
                valid_moves.append('up mirror')
            elif((self.board.map[from_row-1][from_col]=='Red') or (self.board.map[from_row-1][from_col]=='Blue') or (self.board.map[from_row-1][from_col]== 'Yellow')):
                valid_moves.append('up')
            elif(str(self.board.map[from_row-1][from_col])[:6]!='Portal'):
                if(ghost.color!=self.board.map[from_row-1][from_col].color):
                    valid_moves.append('up')
            

        #DOWN
        if(from_row + 1 < self.size):
            if(str(self.board.map[from_row+1][from_col])[:6]=='Mirror'):
                valid_moves.append('down mirror') 
            elif((self.board.map[from_row+1][from_col]=='Red') or (self.board.map[from_row+1][from_col]=='Blue') or (self.board.map[from_row+1][from_col]== 'Yellow')):
                valid_moves.append('down')
            elif(str(self.board.map[from_row+1][from_col])[:6]!='Portal'):
                if(ghost.color!=self.board.map[from_row+1][from_col].color):
                    valid_moves.append('down')
        
        #LEFT
        if(from_col - 1 >= 0):
            if(str(self.board.map[from_row][from_col-1])[:6]=='Mirror'):
                valid_moves.append('left mirror')
            elif((self.board.map[from_row][from_col-1]=='Red') or (self.board.map[from_row][from_col-1]=='Blue') or (self.board.map[from_row][from_col-1]== 'Yellow')):
                valid_moves.append('left')
            elif(str(self.board.map[from_row][from_col-1])[:6]!='Portal'):
                if(ghost.color!=self.board.map[from_row][from_col-1].color):
                    valid_moves.append('left')
            
        #RIGHT
        if(from_col + 1 < self.size):
            if(str(self.board.map[from_row][from_col+1])[:6]=='Mirror'):
                valid_moves.append('right mirror')
            elif((self.board.map[from_row][from_col+1]=='Red') or (self.board.map[from_row][from_col+1]=='Blue') or (self.board.map[from_row][from_col+1]== 'Yellow')):
                valid_moves.append('right')
            elif(str(self.board.map[from_row][from_col+1])[:6]!='Portal'):
                if(ghost.color!=self.board.map[from_row][from_col+1].color):
                    valid_moves.append('right')
            
        
        return valid_moves
    
    def change_player(self):
        if(self.curr_player.number == 1):
            self.curr_player = self.players[1]
        else:
            self.curr_player = self.players[0]

    
    def evaluate(self,board,player):
        score = 0
        opponent = 1 if player == 2 else 2

        # Count the number of ghosts remaining for the player and opponent
        player_ghosts = 0
        opponent_ghosts = 0
        for row in board:
            for cell in row:
                if cell != 0 and str(cell)[-1] == str(player):
                    player_ghosts += 1
                elif cell != 0 and str(cell)[-1] == str(opponent):
                    opponent_ghosts += 1
        score += (player_ghosts - opponent_ghosts) * 10
        
        opponent-=1
        player-= 1
        #print(len(self.players[player].ghostsReleased))
        #print(len(self.players[opponent].ghostsReleased))
        if(len(self.players[player].ghostsReleased)>len(self.players[opponent].ghostsReleased)):
            score+= 150
        

        return score
    

    def minimax(self, depth, is_max_player, alpha, beta,minimax_player):
        if depth == 10 or self.check_win():
            score = self.evaluate(self.temp_board.map, minimax_player)
            if is_max_player:
                return -1, None
            else:
                return 1, None

        best_score = float('-inf') if is_max_player else float('inf')
        best_move = None

        for row1 in self.temp_board.map:
            for ghost in row1:
                if(minimax_player==1):
                    if (str(ghost)[-1]!= '1' or str(ghost)[:6]=='Mirror' or str(ghost)[:6]=='Portal'):
                        continue
                
                if(minimax_player==2):
                    if (str(ghost)[-1]!= '2' or str(ghost)[:6]=='Mirror' or str(ghost)[:6]=='Portal'):
                        continue
                
                #row, col = ghost.position
                row = self.temp_board.map.index(row1)
                col = row1.index(ghost)

                moves = self.valid_moves(row, col, ghost)
                #print(row,col,moves)

                for move in moves:

                    if move.endswith('mirror'):
                        continue

                    # make move
                    if move == 'up':
                        self.temp_board.move_ghost(row, col, move)
                    elif move == 'down':
                        self.temp_board.move_ghost(row, col, move)
                    elif move == 'left':
                        self.temp_board.move_ghost(row, col, move)
                    elif move == 'right':
                        self.temp_board.move_ghost(row, col, move)
                    

                    # recurse
                    self.change_player()
                    
                    score, _ = self.minimax(depth + 1, not is_max_player, alpha, beta,minimax_player)
                    self.change_player()

                    # undo move
                    if move == 'up':
                        self.temp_board.move_ghost(row, col, 'down')
                    elif move == 'down':
                        self.temp_board.move_ghost(row, col, 'up')
                    elif move == 'left':
                        self.temp_board.move_ghost(row, col, 'right')
                    elif move == 'right':
                        self.temp_board.move_ghost(row, col, 'left')

                    
                    if is_max_player:
                        if score > best_score:
                            best_score = score
                            best_move = [row, col, move]
                            alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = [row, col, move]
                            beta = min(beta, best_score)
                        if beta <= alpha:
                            break

        return best_score, best_move






gameMode = -1
while (True):
    print("\tMenu")
    print("0 - Exit")
    print("1 - Player vs Player")
    print("2 - Player vs AI Minimax")
    print("3 - AI Minimax vs AI Minimax")

    gameMode = int(input("Option: "))

    if(gameMode < 0 or gameMode > 4):
        print("\nInvalid option\nTry again\n")
        continue
    if(gameMode == 0): 
        sys.exit(0)
    if(gameMode == 1): 
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
                        
                game.board.released.clear()  
                
                print('Player 1 released ghosts:', end = '\n')
                if (len(game.players[0].ghostsReleased)>0):
                    for i in range(len(game.players[0].ghostsReleased)):
                        print(game.players[0].ghostsReleased[i], end='\n')

                print('Player 2 released ghosts:', end = '\n')
                if(len(game.players[1].ghostsReleased)>0):
                    for i in range(len(game.players[1].ghostsReleased)):
                        print(game.players[1].ghostsReleased[i], end='\n')


                game.players[0].player_score = len(game.players[0].ghostsReleased)
                game.players[1].player_score = len(game.players[1].ghostsReleased)


                game.change_player()

            else:
                continue
            
            if(game.check_win()==True):
                break




    if (gameMode==2):
        game = Game()

        while(True):


            game.board.print_board()   
            if(game.curr_player==game.players[0]):
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

                        if(game.board.release_dungeon(released)):
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
                            
                    game.board.released.clear()  
                    
                    print('Player 1 released ghosts:', end = '\n')
                    if (len(game.players[0].ghostsReleased)>0):
                        for i in range(len(game.players[0].ghostsReleased)):
                            print(game.players[0].ghostsReleased[i], end='\n')

                    print('Player 2 released ghosts:', end = '\n')
                    if(len(game.players[1].ghostsReleased)>0):
                        for i in range(len(game.players[1].ghostsReleased)):
                            print(game.players[1].ghostsReleased[i], end='\n')


                    game.players[0].player_score = len(game.players[0].ghostsReleased)
                    game.players[1].player_score = len(game.players[1].ghostsReleased)


                    game.change_player()

                else:
                    continue

            else:

                """ for i in range(len(game.board.dungeon)):
                    if(str(game.board.dungeon[i])[-1]=='2'):
                        game.board.release_dungeon(game.board.dungeon[i])
                        break """

                for row in game.board.map:
                    for ghost in row:
                        game.temp_board.map[game.board.map.index(row)][row.index(ghost)] = ghost

                
                evaluation, bestMove = game.minimax(9, True, float('+inf'), float('-inf'), 2)
                
                print("Best move = {}".format(bestMove))

                if(bestMove is None):
                    break


                game.board.move_ghost(bestMove[0],bestMove[1],bestMove[2])

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
                        
                game.board.released.clear()  
                
                print('Player 1 released ghosts:', end = '\n')
                if (len(game.players[0].ghostsReleased)>0):
                    for i in range(len(game.players[0].ghostsReleased)):
                        print(game.players[0].ghostsReleased[i], end='\n')

                print('Player 2 released ghosts:', end = '\n')
                if(len(game.players[1].ghostsReleased)>0):
                    for i in range(len(game.players[1].ghostsReleased)):
                        print(game.players[1].ghostsReleased[i], end='\n')


                game.players[0].player_score = len(game.players[0].ghostsReleased)
                game.players[1].player_score = len(game.players[1].ghostsReleased)


                game.change_player()

            
            if(game.check_win()==True):
                break
        


            

    if (gameMode==3):
        game = Game()
        
        while(True):
            game.board.print_board()  
            if(game.curr_player==game.players[0]):
                print('-----------Player 1-----------')
                """ for i in range(len(game.board.dungeon)):
                        if(str(game.board.dungeon[i])[-1]=='1'):
                            game.board.release_dungeon(game.board.dungeon[i])
                            break """

                for row in game.board.map:
                        for ghost in row:
                            game.temp_board.map[game.board.map.index(row)][row.index(ghost)] = ghost

                
                evaluation, bestMove = game.minimax(3, True, float('+inf'), float('-inf'),1)
                
                print("Best move = {}".format(bestMove))

                if(bestMove is None):
                    continue

                game.board.move_ghost(bestMove[0],bestMove[1],bestMove[2])

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
                        
                game.board.released.clear()  
                
                print('Player 1 released ghosts:', end = '\n')
                if (len(game.players[0].ghostsReleased)>0):
                    for i in range(len(game.players[0].ghostsReleased)):
                        print(game.players[0].ghostsReleased[i], end='\n')

                print('Player 2 released ghosts:', end = '\n')
                if(len(game.players[1].ghostsReleased)>0):
                    for i in range(len(game.players[1].ghostsReleased)):
                        print(game.players[1].ghostsReleased[i], end='\n')


                game.players[0].player_score = len(game.players[0].ghostsReleased)
                game.players[1].player_score = len(game.players[1].ghostsReleased)


                game.change_player()

            
                if(game.check_win()==True):
                    break
       
            else:
                print('-----------Player 2-----------')
                """ if(for i in range(len(game.board.dungeon)):
                        if(str(game.board.dungeon[i])[-1]=='2'):
                            game.board.release_dungeon(game.board.dungeon[i])
                            break """

                for row in game.board.map:
                        for ghost in row:
                            game.temp_board.map[game.board.map.index(row)][row.index(ghost)] = ghost

                
                evaluation, bestMove = game.minimax(3, True, float('+inf'), float('-inf'),2)
                
                print("Best move = {}".format(bestMove))
                if(bestMove is None):
                    continue


                game.board.move_ghost(bestMove[0],bestMove[1],bestMove[2])

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
                        
                game.board.released.clear()  
                
                print('Player 1 released ghosts:', end = '\n')
                if (len(game.players[0].ghostsReleased)>0):
                    for i in range(len(game.players[0].ghostsReleased)):
                        print(game.players[0].ghostsReleased[i], end='\n')

                print('Player 2 released ghosts:', end = '\n')
                if(len(game.players[1].ghostsReleased)>0):
                    for i in range(len(game.players[1].ghostsReleased)):
                        print(game.players[1].ghostsReleased[i], end='\n')


                game.players[0].player_score = len(game.players[0].ghostsReleased)
                game.players[1].player_score = len(game.players[1].ghostsReleased)


                game.change_player()

            
                if(game.check_win()==True):
                    break

