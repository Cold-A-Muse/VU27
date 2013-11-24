__author__ = 'Helsloot'


class NumberRow(object):

    def __init__(self):
        self.row_weaver = []

    def __str__(self):
        return " ".join(self.row_weaver[i] for i in range(len(self.row_weaver)))

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.row_weaver[key]

    def __len__(self):
        return self.row_weaver.__len__()

    def add(self, row_one_number, row_two_number):
        self.row_weaver.append(row_one_number)
        self.row_weaver.append(row_two_number)

    def weave(self, row):
        self.row_weaver.append(row)