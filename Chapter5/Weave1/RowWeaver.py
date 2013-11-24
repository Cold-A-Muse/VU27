__author__ = 'Helsloot'


class RowWeaver(object):

    def __init__(self):
        self.row_weaver = []

    def __str__(self):
        return " ".join(self.row_weaver[i] for i in range(len(self.row_weaver)))

    def __repr__(self):
        return str(self)

    def add(self, row_one_number, row_two_number):
        self.row_weaver.append(row_one_number)
        self.row_weaver.append(row_two_number)
