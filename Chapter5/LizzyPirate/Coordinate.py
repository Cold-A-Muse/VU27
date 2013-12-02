'''
Assignment: Pirate - class Coordinate
Created on 2 dec. 2013
Author: Lizzy Sinnema
'''

class Coordinate(object):
    
    def __init__(self, x_of_y):
        self.coordinate = x_of_y
    
    def pas_x_aan(self):
        return str(int(self.coordinate) + 1)