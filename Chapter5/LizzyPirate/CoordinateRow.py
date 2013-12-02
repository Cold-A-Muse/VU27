'''
Assignment: Pirate - class CoordinateRow
Created on 2 dec. 2013
Author: Lizzy Sinnema
'''


class CoordinateRow(object):
    
    def __init__(self):
        self.coordinate_row = []
    
    def add(self, input):  # will add a new getal uit de list to the back of the row
        self.coordinate_row.append(input)
    
    def weave(self, other):
        result = CoordinateRow()
        length = len(self.coordinate_row)
        for i in range(min(length, len(other))):
            result.add(self.coordinate_row[i])
            result.add(other.coordinate_row[i])
        return result