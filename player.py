class Player:
    def __init__(self, number):
        self.number = number
        self.dungeon = []
        self.ghostsReleased = []

    def add_ghost_to_dungeon(self, ghost):
        self.dungeon.append(ghost)

    def remove_ghost(self, ghost):
        self.ghosts.remove(ghost)

    def __str__(self):
        return f"Player {self.number}"

    # def get_move(self, game):
    #     # This method should return a move object based on the player's input
