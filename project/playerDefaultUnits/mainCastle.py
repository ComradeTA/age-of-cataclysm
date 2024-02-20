from gameworldDefaults.building import Building

class MainCastle(Building):
    def __init__(self, health_points=1):
        super().__init__(health_points)
    
    def process(self, game):
        return super().process(game)
        

    