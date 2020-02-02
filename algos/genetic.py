import copy
import random
import math
from utils.solution import Solution
from map.map import Map

class Genetic:

    def __init__(self):
        self.steps = 0

    def solve(self, map, num_colors, problem_size):
        self.problem_size = problem_size
        self.original_temp = 10
        self.temperature = self.original_temp
        self.population = []
        self.num_colors = num_colors
        self.temperature = 10
        self.fittest = None
        self.map = map
        self.setup(map, num_colors)
        return self.run_algo()

    def setup(self, map, num_colors):
        # Parameter that can be adjusted
        pop_size = 20

        for i in range(pop_size):
            map_copy = copy.deepcopy(map)
            for country in map_copy.countries:
                country.set_valid_colors(range(num_colors))
                country.set_color(random.choice(country.get_valid_colors()))
            solution = Solution(map_copy, num_colors)
            solution.determine_fitness()
            self.population.append(solution)

    def run_algo(self):
        # Parameter that can be adjusted
        run_times = 100
        self.fittest = copy.deepcopy(self.population[0])

        for i in range(run_times):
            # Check if we have a valid solution
            for solution in self.population:
                #if(solution.is_valid and solution.get_num_colors_used()):
                if(solution.is_valid):
                    solution.steps = self.steps
                    print(f'returned from here {self.steps}')
                    return solution

            # Get'er done
            tournament_results = self.generate_tournaments()
            new_population = self.select_and_mate(tournament_results)
            self.population = self.select_parent_to_persist(self.population, new_population)
            self.steps += 1
        return self.fittest

    def heat_function(self):
        # Parameter that can be adjusted
        tao = 0.97
        self.temperature = self.temperature * tao
        if(self.temperature < 0.0015):
            self.temperature = 0.0015
        return self.temperature

    def generate_tournaments(self):
        winners = []
        losers = []

        # Tournament size is set to two
        for i in range(int(len(self.population)/2)):
            contestant_one = random.choice(self.population)
            contestant_two = random.choice(self.population)

            #self.population.remove(contestant_one)
            #if contestant_two in self.population:
            #    self.population.remove(contestant_two)

            contestant_one_fitness = contestant_one.get_fitness()
            contestant_two_fitness = contestant_two.get_fitness()

            if contestant_one_fitness < contestant_two_fitness:
                winners.append({'contestant': copy.deepcopy(contestant_one), 'position': 'winner'})
                losers.append({'contestant': copy.deepcopy(contestant_two), 'position': 'loser'})
            else:
                winners.append({'contestant': copy.deepcopy(contestant_two), 'position': 'winner'})
                losers.append({'contestant': copy.deepcopy(contestant_one), 'position': 'loser'})

        # Set the population back to what it was before the
        # tournaments
        #self.population.extend([winner['contestant'] for winner in winners])
        #self.population.extend([loser['contestant'] for loser in losers])

        return {
            'winners': winners,
            'losers': losers
        }

    def select_and_mate(self, tournament_results):
        # At this point, we should have pop_size/two (10)
        # in each array in the tournament_results
        
        # Parents have form:
        # {
        #   'contestant': contestant_one,
        #   'position': 'winner'
        # }
        new_generation = []
        children_per_couple = 2
        for i in range(int(len(tournament_results['winners'])/2)):
            parent_one = random.choice(tournament_results['winners'])['contestant']
            parent_two = random.choice(tournament_results['winners'])['contestant']
            for j in range(children_per_couple):
                self.mate(parent_one, parent_two, new_generation)

        for i in range(int(len(tournament_results['losers'])/2)):
            parent_one = random.choice(tournament_results['losers'])['contestant']
            parent_two = random.choice(tournament_results['losers'])['contestant']
            for j in range(children_per_couple):
                self.mate(parent_one, parent_two, new_generation)

        return new_generation

    def mate(self, parent, other_parent, new_generation):
        child = Solution(copy.deepcopy(parent.map), self.num_colors)
        chance_of_mutation = 0.05

        for i in range(len(child.map.countries)):
            swap = random.uniform(0, 1)
            if swap <= 0.5:
                parent_color = other_parent.map.countries[i].get_color()
                child.map.countries[i].set_color(parent_color)
            if random.uniform(0, 1) <= chance_of_mutation:
                random.choice(child.map.countries).set_color(random.choice(range(child.num_colors_available)))
        new_generation.append(child)

    def select_parent_to_persist(self, old_generation, new_generation):
        # Make sure that everyone's fitness is updated (old_generation is, but younger is not)
        # Select a parent to persist(as temp decreases, chose better parents)
        # Select a child to end (as temp decreases, chose worse children)
   
        fitest_parent = copy.deepcopy(old_generation[0])
        fitest_parent.determine_fitness()
        for individual in old_generation:
            individual.determine_fitness()
            if individual.get_fitness() < fitest_parent.get_fitness():
                fitest_parent = copy.deepcopy(individual)

        weakest_child = new_generation[0]
        weakest_child.determine_fitness()
        for individual in new_generation:
            individual.determine_fitness()
            if individual.get_fitness() > weakest_child.get_fitness():
                weakest_child = individual

        new_generation.remove(weakest_child)
        new_generation.append(fitest_parent)

        for child in new_generation:
           if child.get_fitness() < self.fittest.get_fitness():
               print(f"updated_fittest on step {self.steps}")
               self.fittest = copy.deepcopy(child)

        counter = 0
        for child in new_generation:
            print(child.get_fitness())
            if round(child.get_fitness(),4) == round(new_generation[0].get_fitness(),4):
                counter += 1
        print("----------------------------------")

        if counter >= len(new_generation):
            print(f"We converged: {self.steps}")
            raise ValueError
        
        return new_generation
