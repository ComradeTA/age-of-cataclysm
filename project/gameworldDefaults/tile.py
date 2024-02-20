class Tile:
    def __init__ (self, texture, walkable, changeable):
        self.texture = texture
        self.walkable = walkable
        self.changeable = changeable

    def change_Texture(self, new_texture):
        self.texture = new_texture

    def change_Walkable(self, bool_walkable):
        self.walkable = bool_walkable