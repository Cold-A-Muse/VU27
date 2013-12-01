__author__ = 'Helsloot'


class Coordinate(str):

    def __init__(self, input):
        self.coord = input

    def getX(self):
        split = self.split(',')
        return split[0]

    def getAdjustedX(self):
        split = self.split(',')
        old_x = int(split[0])
        new_x = old_x + 1
        return new_x

    def getY(self):
        split = self.split(',')
        return split[1]