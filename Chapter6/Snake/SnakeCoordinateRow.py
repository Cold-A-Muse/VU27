__author__ = 'Helsloot'


class SnakeCoordinateRow(object):

    def __init__(self):
        self.snake_tail = []

    def add(self, part):
        self.snake_tail.append(part)

    def remove(self):
        self.snake_tail.pop(0)