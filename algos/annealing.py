import copy
import random
import math
from utils.solution import Solution
from map.map import Map

class Annealing:
    
    def __init__(self):
        self.run_times = 3000
        self.temperature = 10
        self.steps = 0
        # List for countries that couldn't be colored
        # and need to go back onto the queue at some
        # point
    
    def solve(self, map, num_colors):
        self.map = map
        self.num_colors = num_colors
        self.setup(map, num_colors)
        best_soln = copy.deepcopy(self.soln)
        best_soln.determine_fitness()
        if best_soln.get_fitness() < 1:
            return best_soln
        for i in range(self.run_times):
            curr_country_node = random.choice(self.soln.map.countries)
            best = self.set_best_color(curr_country_node)
            # Fitness is updated in self.set_best_color
            # Careful, self.soln and best point to same object
            if best.get_fitness() < 1:
                return best
            if best.get_fitness() < best_soln.get_fitness():
                best_soln = copy.deepcopy(best)
            self.steps += 1
            # No longer matters
        self.soln.steps = self.steps
        return best_soln
    
    def setup(self, map, num_colors):
        self.soln = Solution(map, num_colors, "Annealing")
        self.set_map()

    def set_best_color(self, curr_country_node):
        self.soln.determine_fitness()
        orig_best_score = self.soln.get_fitness()
        best = copy.deepcopy(self.soln)
        best_colors = self.copy_colors(best.map.countries)
        orig_color = curr_country_node.get_color()
        for color in curr_country_node.get_valid_colors():
            curr_country_node.set_color(color)
            self.soln.determine_fitness()
            if self.soln.get_fitness() < best.get_fitness():
                best = copy.deepcopy(self.soln)
                best_colors = self.copy_colors(self.soln.map.countries)

        if best.get_fitness() == orig_best_score:
            counter = 0
            fitness_with_rand = orig_best_score
            self.copy_back_colors(best_colors, self.soln.map.countries)

            while fitness_with_rand == orig_best_score and counter < len(curr_country_node.get_valid_colors()) + 5:
                random_color = random.choice(curr_country_node.get_valid_colors())
                curr_country_node.set_color(random_color)
                self.soln.determine_fitness()
                fitness_with_rand = self.soln.get_fitness()
                counter += 1

            stat = math.exp(-((fitness_with_rand - orig_best_score) / (1.38064852 * self.heat_function())))
            if random.uniform(0, 1) > stat:
                curr_country_node.set_color(orig_color)
            self.soln.determine_fitness()
            best = copy.deepcopy(self.soln)
            best_colors = self.copy_colors(self.soln.map.countries)
        self.copy_back_colors(best_colors, self.soln.map.countries)
        return best

    def set_map(self):
        for country in self.map.countries:
            country.set_valid_colors(range(self.num_colors))
            country.set_color(random.choice(country.get_valid_colors()))

    def heat_function(self):
        # Parameter that can be adjusted
        tao = 0.97
        self.temperature = self.temperature * tao
        if(self.temperature < 0.0015):
            self.temperature = 1
        return self.temperature

    def copy_colors(self, map_arr):
        ret_array = []
        for country in map_arr:
            ret_array.append(country.get_color())
        return ret_array

    def copy_back_colors(self, pull_from, countries_to_color):
        for i, country in enumerate(countries_to_color):
            country.set_color(pull_from[i])
