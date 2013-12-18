'''
Assignment: Snake
Class: SnakeCoordinateRow
Created on 8th of december 2013
Author: Daan Helsloot (dht340)
'''
from Coordinate import Coordinate

class SnakeCoordinateRow(object):

    def __init__(self):
        self.snake_tail = []

    def add(self, part):
        self.snake_tail.append(part)

    def add_coord(self, x, y):
        self.snake_tail.append(Coordinate(x, y))

    def remove(self):
        return self.snake_tail.pop(0)