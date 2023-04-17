from position import *

class Ghost:
    
    def __init__(self, color, symbol, position):
        self.color = color
        self.symbol = symbol
        self.position = position
        self.dungeon = False

    def get_color(self):
        return self.color

    def __repr__(self):
        return f"{self.color} {self.symbol}"
    
    def __str__(self):
        return f"{self.color} {self.symbol}"

    def get_ghost(self, row, col):
        
        return 