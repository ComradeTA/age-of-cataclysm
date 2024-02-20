from gameworldDefaults.actor import Actor

class Pawn(Actor):
    def __str__(self, health_points = 1):
            return "Player " + str(self.id)
            self.velocity = 3
            self.direction_vector = [0, 0]
            self.health_points = health_points
