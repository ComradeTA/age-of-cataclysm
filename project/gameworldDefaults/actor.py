class Actor():
    def __init__(self, id, name,  x = 0, y = 0, model = 0, size = 1, scale = 1):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.scale = scale
        self.model = model

    def __str__(self):
        return "Player " + str(self.id)
    

    def process(self, game):
        pass