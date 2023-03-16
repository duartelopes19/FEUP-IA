from position import *

class Ghost:
    
    def __init__(self, color, symbol, position):
        self.color = color
        self.symbol = symbol
        self.position = position
        self.dungeon = False

    def __repr__(self):
        return f"{self.color} {self.symbol}"