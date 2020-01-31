import copy
import random
import math
from utils.solution import Solution
from map.map import Map

class Genetic:

    def solve(self, map, num_colors):
        self.original_temp = 10
        self.temperature = self.original_temp
        self.population = []
        self.num_colors = num_colors
        self.temperature = 10
        self.steps = 0
        self.fittest = None
        self.map = map
        self.setup(map, num_colors)
        return self.run_algo()

    def setup(self, map, num_colors):
        # Parameter that can be adjusted
        pop_size = 20

        for i in range(pop_size):
            map_copy = copy.deepcopy(map)
            for country in map_copy:
                country.set_color(random.choice(country.get_valid_colors()))
            solution = Solution(map_copy, num_colors)
            solution.determine_fitness()
            self.population.append(solution)

    def run_algo(self):
        # Parameter that can be adjusted
        run_times = 1000
        self.fittest = self.population[0]

        for i in range(run_times):
            # Check if we have a valid solution
            for solution in self.population:
                if(solution.is_valid and solution.get_num_colors_used == 3):
                    solution.steps = self.steps
                    return solution

            # Get'er done
            tournament_results = self.generate_tournaments()
            new_population = self.select_and_mate(tournament_results)
            self.population = self.select_parent_to_persist(self.population, new_population)
            self.steps += 1

    def heat_function(self):
        # Parameter that can be adjusted
        tao = 0.97
        self.temperature = self.temperature * tao
        return self.temperature

    def generate_tournaments(self):
        winners = []
        losers = []

        # Tournament size is set to two
        for i in range(int(len(self.population)/2)):
            contestant_one = random.choice(self.population)
            contestant_two = random.choice(self.population)

            self.population.remove(contestant_one)
            self.population.remove(contestant_two)

            contestant_one_fitness = contestant_one.get_fitness()
            contestant_two_fitness = contestant_two.get_fitness()

            if contestant_one_fitness < contestant_two_fitness:
                winners.append({'contestant': contestant_one, 'position': 'winner'})
                losers.append({'contestant': contestant_two, 'position': 'loser'})
            else:
                winners.append({'contestant': contestant_two, 'position': 'winner'})
                losers.append({'contestant': contestant_one, 'position': 'loser'})

        # Set the population back to what it was before the
        # tournaments
        self.population.append(winners).append(losers)
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
        all_parents = tournament_results['winners'].copy().append(tournament_results['losers'].copy())
        random.shuffle(all_parents)
        for parent in all_parents:
            group_assignment = random.randrange(0, 1, 0.01)
            # Parameter that can be adjusted
            bench_mark = math.exp(1/self.heat_function())

            if parent['position'] == 'winner':
                first_pool = tournament_results['winners']
            else:
                first_pool = tournament_results['losers']
            if group_assignment > bench_mark:
                other_parent = random.choice(first_pool)
                all_parents.remove(other_parent)
                first_pool.remove(other_parent)
            else:
                other_parent = random.choice(all_parents)
                all_parents.remove(other_parent)

            for i in range(children_per_couple-1):
                self.mate(parent, other_parent, new_generation)

        return new_generation

    def mate(self, parent, other_parent, new_generation):
        # By starting at index one, we ensure that at least one gene
        # comes from each parent
        cross_point = random.randint(1, len(parent.map.countries))
        child = Solution(parent.map, self.num_colors)

        # By having a range of the cross_point, we can ensure that
        # at least one "gene" comes from both parents
        for i in range(cross_point):
            parent_color = other_parent.map.countries[i].get_color()
            child.map.countries[i].set_color(parent_color)
        new_generation.append(child)

    def select_parent_to_persist(self, old_generation, new_generation):
        # Make sure that everyone's fitness is updated (old_generation is, but younger is not)
        # Select a parent to persist(as temp decreases, chose better parents)
        # Select a child to end (as temp decreases, chose worse children)
        for individual in new_generation:
            individual.determine_fitness()

        parent_choices = []

        for parent in old_generation:
            stat = (-(0.1 * parent.get_fitness()) / (0.9 * (self.original_temp + 0.1 - self.heat_function)))
            for i in range(int(round(stat,4)*100)-1):
                parent_choices.append(parent)
   
        parent_to_keep = random.choice(parent_choices)

        child_choices = []

        for child in new_generation:
            stat = -(10 + self.heat_function() / math.sqrt(child.get_fitness()))
            for i in range(int(round(stat,4)*100)-1):
                child_choices.append(child)

        child_to_remove = random.choice(child_choices)
        child_choices.remove(child_to_remove)
        child_choices.append(parent_to_keep)

        return child_choices