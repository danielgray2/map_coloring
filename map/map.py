# pylint: disable=relative-beyond-top-level

from math import sqrt, isinf
import random
import numpy as np
from .country import Country
from .border import Border

class Map():
    '''
    This class is responsible for handling a map
    object that consists of countries and borders
    '''
    def __init__(self, num_countries):
        self.countries = []
        self.borders = []
        self.x_positions = list(np.delete(np.linspace(0, 1, 1000), 1))
        self.y_positions = list(np.delete(np.linspace(0, 1, 1000), 1))

        for i in range(num_countries):
            self.countries.append(Country(self.x_positions, self.y_positions))
        self.draw_borders()
    
    def get_intersects(self, new_border):
        new_border_equation = new_border.get_equation()
        intersections = []
        for border in self.borders:
            extremes = border.get_extremes()
            border_equation = border.get_equation()
            try:
                x = (new_border_equation['intercept'] - border_equation['intercept']) / (border_equation['slope'] - new_border_equation['slope'])
                y = new_border_equation['slope'] * x + new_border_equation['intercept']
                if round(x, 4) >= round(extremes['left'], 4) and round(x, 4) <= round(extremes['right'], 4) and round(y, 4) >= round(extremes['bottom'], 4) and round(y, 4) <= round(extremes['top'], 4):
                    intersections.append({'x': x, 'y': y})
            except ZeroDivisionError:
                x = new_border.country_a.x
                y = border_equation['slope'] * x + border_equation['intercept']
                if round(x, 4) >= round(extremes['left'], 4) and round(x, 4) <= round(extremes['right'], 4) and round(y, 4) >= round(extremes['bottom'], 4) and round(y, 4) <= round(extremes['top'], 4):
                    intersections.append({'x': x, 'y': y})
        return intersections

    def check_distance(self, intersects, new_border):
        # Get distance between the two new points and
        # compare that to the distance between one of the
        # new points and the intersection
        new_point_a = new_border.country_a
        new_point_b = new_border.country_b

        new_distance = sqrt(pow(new_point_a.x - new_point_b.x, 2) + pow(new_point_a.y - new_point_b.y, 2))
        for intersect in intersects:
            dist_from_a = sqrt(pow(new_point_a.x - intersect['x'], 2) + pow(new_point_a.y - intersect['y'], 2))
            dist_from_b = sqrt(pow(new_point_b.x - intersect['x'], 2) + pow(new_point_b.y - intersect['y'], 2))
            if round(dist_from_a, 4) > round(dist_from_b, 4):
                intersect_distance = dist_from_a
            else:
                intersect_distance = dist_from_b


            if round(new_distance, 4) > round(intersect_distance, 4):
                return False

        return True

    def can_draw_border(self, new_border):
        intersects = self.get_intersects(new_border)
        if len(intersects) > 0:
            what_should_we_return = self.check_distance(intersects, new_border)
            return what_should_we_return
        return True

    def draw_borders(self):
        draw_borders_for = self.countries[:]

        while len(draw_borders_for) > 0:
            cur_index = random.randint(0, len(draw_borders_for)-1)
            country_one = draw_borders_for.pop(cur_index)
            neighbor_set = set(country_one.neighbors)
            not_neighbor_set = set(country_one.not_neighbors)
            options_set = set(self.countries[:])
            possible_values = list(options_set.difference(neighbor_set).difference(not_neighbor_set))
            possible_values.remove(country_one)
            new_border = Border()
            valid_border = False

            while len(possible_values) > 0 and not valid_border:
                cur_index = self.find_closest(country_one, possible_values)
                country_two = possible_values.pop(cur_index)
                new_border.draw_test_border(country_one, country_two)
                valid_border = self.can_draw_border(new_border)

            if len(possible_values) > 0:
                draw_borders_for.append(country_one)

            if valid_border:
                new_border.draw_border(country_one, country_two)
                self.borders.append(new_border)
            else:
                country_one.add_not_neighbor(country_two)


    def find_closest(self, country, country_list):
        closest_dist = 10000000
        cur_closest = None
        for item in country_list:
            if self.calc_distance(country, item) < closest_dist:
                cur_closest = item
        return country_list.index(cur_closest)


    def calc_distance(self, country_a, country_b):
        return sqrt(pow(country_a.x - country_b.x, 2) + pow(country_a.y - country_b.y, 2))