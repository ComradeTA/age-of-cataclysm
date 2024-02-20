from gameworldDefaults.character import Character
from gameworldDefaults.gameData import GameData

class Game():
    def __init__(self, name, seed, id, host, multiplayer=False):
        self.name = name
        self.id = id
        self.host = host
        self.multiplayer = multiplayer
        self.gameData = GameData(seed)
        
    def __str__(self):
        return str(self.name) + str(self.gameData.characters)

    def play(self, data):
        p = data[0]
        move = data[1]
        for character in self.gameData.characters:
            if character.id == p:
                character.character_move(move)

    def add_player(self, p, n):
        self.gameData.add_player(Character(p, n))

    def remove_player(self, p):
        for character in self.gameData.characters:
            if character.id == p:
                self.gameData.remove_player(character)
        
