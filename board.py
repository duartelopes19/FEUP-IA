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