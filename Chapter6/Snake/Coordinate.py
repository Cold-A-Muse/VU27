'''
Assignment: Snake
Class: Coordinate
Created on 8th of december 2013
Author: Daan Helsloot (dht340)
'''


class Coordinate(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def shift(self, x, y):
        self.x += x
        self.y += y