class Border():
    '''
    This class is responsible for handling a border
    object
    '''
    def __init__(self):
        self.country_a = None
        self.country_b = None
        self.intercept = None
        self.slope = None

    def find_equation(self):
        '''
        Finds the equation of a line between
        two countries. This is the equation
        of the border.
        '''
        if self.country_a and self.country_b:
            x1 = self.country_a.x
            x2 = self.country_b.x
            y1 = self.country_a.y
            y2 = self.country_b.y

            if x1 - x2 == 0:
                self.slope = 1000003
            else:
                self.slope = (y1-y2)/(x1-x2)
            self.intercept = y1 - (self.slope*x1)

        else:
            self.slope = None
            self.intercept = None
    
    def get_equation(self):
        return {
            "slope": self.slope,
            "intercept": self.intercept
        }
        
    def draw_border(self, country_a, country_b):
        '''
        Draws a border between two countries
        '''
        self.country_a = country_a
        self.country_b = country_b
        
        self.country_a.add_neighbor(country_b)
        self.country_b.add_neighbor(country_a)

        self.find_equation()
    
    def draw_test_border(self, country_a, country_b):
        '''
        Draws a border but does not change the neighbors
        arrays for either of the countries
        '''
        self.country_a = country_a
        self.country_b = country_b

        self.find_equation()

    def get_other_country(self, country):
        '''
        To be used by countries to get the country
        on the other side of the border.
        '''
        if self.country_a != country:
            return self.country_a
        return self.country_b
    
    def get_extremes(self):
        '''
        This returns the locations of the country
        furthest right, left, up, and down
        '''
        return_obj = {
            'top': None,
            'bottom': None,
            'left': None,
            'right': None
        }

        if self.country_a.y <= self.country_b.y:
            return_obj['bottom'] = self.country_a.y
            return_obj['top'] = self.country_b.y
        else:
            return_obj['top'] = self.country_a.y
            return_obj['bottom'] = self.country_b.y
        if self.country_a.x <= self.country_b.x:
            return_obj['left'] = self.country_a.x
            return_obj['right'] = self.country_b.x
        else:
            return_obj['left'] = self.country_b.x
            return_obj['right'] = self.country_a.x

        return return_obj