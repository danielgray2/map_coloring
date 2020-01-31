class Solution():
    def __init__(self, map, num_colors):
        self.map = map
        self.num_colors_available = num_colors
        self.num_colors_used = 0
        self.num_conflicts = 0
        self.steps = 0
        self.num_conflicts = -1
        self.is_valid = False
        self.set_valid_colors(num_colors)

    def get_num_conflicts(self):
        self.num_conflicts = 0
        for country in self.map.countries:
            neighbors = country.neighbors
            for neighbor in neighbors:
                if neighbor.color == country.color:
                    self.num_conflicts += 1

        # Divide num_conflicts by two because we
        # have counted each one twice
        self.num_conflicts = self.num_conflicts/2

        if self.num_conflicts > 0:
            self.is_valid = False
        elif self.num_conflicts == 0:
            self.is_valid = True
        return self.num_conflicts

    def set_valid_colors(self, num_colors):
        if num_colors == 3:
            valid_colors = range(2)
        elif num_colors == 4:
            valid_colors = range(3)
        for country in self.map.countries:
            country.set_valid_colors(valid_colors)

    def get_num_colors_used(self):
        colors_used = []
        for country in self.map.countries:
            if country.get_color() not in colors_used:
                colors_used.append(country.get_color)
            if colors_used == self.num_colors_available:
                self.num_colors_used = len(colors_used)
                return self.num_colors_used
        self.num_colors_used = len(colors_used)
        return self.num_colors_used
    
    # TODO: Make sure Elijah likes this fitness function
    def determine_fitness(self):
        conflicts = self.get_num_conflicts()
        colors_used = self.get_num_colors_used()
        self.fitness = conflicts + (colors_used * 0.1)

    def get_fitness(self):
        return self.fitness