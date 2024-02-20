from gameworldDefaults.actor import Actor

class Building(Actor):
    def __init__(self, health_points = 1):
        self.health_points = health_points