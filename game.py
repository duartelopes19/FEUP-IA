class Game:
    def __init__(self):
        self.dungeon = []
        self.players = [Player(1),Player(2)]
        self.curr_player = self.players[0]
        
        # Initialize the board with empty cells
        self.board = 
        
        # Initialize the ghosts
        self.init_ghosts(players[0],"G1")
        self.init_ghosts(players[1],"G2")
        
    def init_ghosts(self, player, symbol):
        # TODO: Implement the initialization of the ghosts
        for i in range(3):
            player.add_ghost(Ghost(red,symbol))
            player.add_ghost(Ghost(yellow,symbol))
            player.add_ghost(Ghost(blue,symbol))

        
    def is_valid_move(self, move):
        # TODO: Implement the check for valid moves
        
    def update_board(self, move):
        # TODO: Implement the update of the board after each move
        
    def is_game_over(self):
        # TODO: Implement the check for game over


class Player:
    def __init__(self, number):
        self.number = number
        self.ghosts = []

    def add_ghost(self, ghost):
        self.ghosts.append(ghost)

    def remove_ghost(self, ghost):
        self.ghosts.remove(ghost)

    def get_move(self, game):
        # This method should return a move object based on the player's input


class Ghost:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

    def __repr__(self):
        return self.symbol


class Board:
    def __init__(self):
        self.size = 5
        self.grid = [
            'B','R','PR','B','R',
            'Y','M','Y','M','Y',
            'R','B','R','B','PY',
            'B','M','Y','M','R',
            'Y','R','PB','B','Y'
        ]

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

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Position({self.x}, {self.y})"