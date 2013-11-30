'''
Assignment: Pirate
Created on 30 nov. 2013
Author: Daan Helsloot
'''


class CoordinateRow(object):

    def __init__(self):
        self.coordinate_row = []

    def add(self, input):
        self.coordinate_row.append(input)

    def weave(self, other):
        result = CoordinateRow()
        length = len(self.coordinate_row)
        for i in range(min(length, len(other))):
            result.add(self.coordinate_row[i])
            result.add(other.coordinate_row[i])
        return result