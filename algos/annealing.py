import copy
import random
import math
from utils.sorted_queue import SortedQueue
from utils.solution import Solution
from map.map import Map

class Annealing:
    
    def __init__(self, map, num_colors):
        self.solutions = []
        self.num_colors = num_colors
        self.steps = 0
        self.solve(map, self.num_colors)
        self.setup(map, self.num_colors)
    
    def setup(self, map, num_colors):
        country_queue = SortedQueue()
        soln = Solution(map, num_colors)
        for country in soln.countries:
            country_queue.add(country)
    
    def solve(self, map, num_colors):
        