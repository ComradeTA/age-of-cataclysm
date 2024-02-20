
class GameData():
    def __init__(self, seed, connected_client_ids = [], active_enemy_ids = [], cached_player_ids = ()):
        self.seed = seed
        self.connected_client_ids = connected_client_ids
        self.active_enemy_ids = active_enemy_ids
        self.cached_player_ids = cached_player_ids
        self.characters = {}
        self.pawns = {}
        self.actors = {}
        self.buildings = {}
        
    def __str__(self):
        return str(self.name) + str(self.characters)

    def add_player(self, character):
        self.characters.append(character)

    def remove_player(self, character):
        self.characters.remove(character)

    def add_pawn(self, pawn):
        self.characters.append(pawn)

    def remove_pawn(self, pawn):
        self.pawn.remove(pawn)

    def add_actor(self, actor):
        self.characters.append(actor)

    def remove_actor(self, actor):
        self.characters.remove(actor)

    def add_building(self, building):
        self.characters.append(building)

    def remove_building(self, building):
        self.characters.remove(building)
    
        
