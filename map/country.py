import random
class Country():
    '''
    This class is responsible for creating a country
    object
    '''
    def __init__(self, x_positions, y_positions):
        # Select random point between 0.001 and 0.999
        # for the country location
        self.x = random.choice(x_positions)
        self.y = random.choice(y_positions)
        self.color = -1
        self.neighbors = []
        self.not_neighbors = []
        self.borders = []
        self.valid_colors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def add_not_neighbor(self, not_neighbor):
        self.not_neighbors.append(not_neighbor)