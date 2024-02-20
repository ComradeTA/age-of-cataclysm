from gameworldDefaults.pawn import Pawn
from gameworldDefaults.gameData import GameData

class Character(Pawn):
    def __str__(self):
            return "Player " + str(self.id)

    def character_move(self, direction):
        if direction == "right":
            #x
            self.x += self.v
        elif direction == "up":
            #-y
            self.y -= self.v
        elif direction == "left":
            #-x
            self.x -= self.v
        elif direction == "down":
            #y
            self.y += self.v