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
            for country in map_copy.countries:
                country.set_valid_colors(range(num_colors))
                country.set_color(random.choice(country.get_valid_colors()))
            solution = Solution(map_copy, num_colors)
            solution.determine_fitness()
            self.population.append(solution)

    def run_algo(self):
        # Parameter that can be adjusted
        run_times = 10000
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
                winners.append({'contestant': contestant_one, 'position': 'winner'})
                losers.append({'contestant': contestant_two, 'position': 'loser'})
            else:
                winners.append({'contestant': contestant_two, 'position': 'winner'})
                losers.append({'contestant': contestant_one, 'position': 'loser'})

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
        all_parents = tournament_results['winners']
        all_parents.extend(tournament_results['losers'])
        random.shuffle(all_parents)
        for i in range(int(len(all_parents)/2)):
            group_assignment = random.uniform(0, 1)
            # Parameter that can be adjusted
            bench_mark = math.exp(-1/self.heat_function())

            if all_parents[i]['position'] == 'winner':
                first_pool = tournament_results['winners']
            else:
                first_pool = tournament_results['losers']
            if group_assignment > bench_mark:
                other_parent = random.choice(first_pool)
                #first_pool.remove(other_parent)
                #all_parents.remove(other_parent)
            else:
                other_parent = random.choice(all_parents)
                #all_parents.remove(other_parent)

            for j in range(children_per_couple):
                self.mate(all_parents[i]['contestant'], other_parent['contestant'], new_generation)

        return new_generation

    def mate(self, parent, other_parent, new_generation):
        # By starting at index one, we ensure that at least one gene
        # comes from each parent
        cross_point = random.randint(1, len(parent.map.countries))
        child = Solution(parent.map, self.num_colors)
        chance_of_mutation = 0.05

        # By having a range of the cross_point, we can ensure that
        # at least one "gene" comes from both parents
        for i in range(cross_point):
            parent_color = other_parent.map.countries[i].get_color()
            child.map.countries[i].set_color(parent_color)
            if random.uniform(0, 1) <= 0.05:
                random.choice(child.map.countries).set_color(random.choice(range(child.num_colors_available)))
        new_generation.append(child)

    def select_parent_to_persist(self, old_generation, new_generation):
        # Make sure that everyone's fitness is updated (old_generation is, but younger is not)
        # Select a parent to persist(as temp decreases, chose better parents)
        # Select a child to end (as temp decreases, chose worse children)
        for individual in new_generation:
            individual.determine_fitness()
        
        for individual in old_generation:
            individual.determine_fitness()

        parent_choices = []

        for parent in old_generation:
           # Lots of parameters to tune
        #    #stat = math.exp(-(0.1 * parent.get_fitness()) / (0.9 * (self.original_temp + 0.1 - self.heat_function())))
           parent_choices.append(parent)
           stat = math.exp(-0.1 * parent.get_fitness() / (self.heat_function()))
           for i in range(int(round(stat,4)*100)):
               parent_choices.append(parent)
   
        parent_to_keep = random.choice(parent_choices)

        child_choices = []

        for child in new_generation:
            # Lots of parameters to tune
            child_choices.append(child)
            stat = math.exp(-(self.heat_function()) / 0.1 * parent.get_fitness())
            for i in range(int(round(stat,4)*100)):
                child_choices.append(child)

        child_to_remove = random.choice(child_choices)
        new_generation.remove(child_to_remove)
        new_generation.append(parent_to_keep)

        for child in new_generation:
           if child.get_fitness() < self.fittest.get_fitness():
               print(f"updated_fittest on step {self.steps}")
               self.fittest = copy.deepcopy(child)

        counter = 0
        for individual in new_generation:
           if individual.get_fitness == new_generation[0].get_fitness():
               counter += 1
        
        return new_generation