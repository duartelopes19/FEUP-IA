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
