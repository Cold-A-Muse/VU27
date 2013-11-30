__author__ = 'Helsloot'
from ipy_lib import file_input
from CoordinateRow import CoordinateRow
from Coordinate import Coordinate

def addAll(coord_row, coordinate_row_instance):
    for i in range(len(coord_row)):
        if '=' in coord_row[i]:

            return coordinate_row_instance.add(coord_row[i].split('=')[0])
        else:
            coordinate_row_instance.add(coord_row[i])
    print coordinate_row_instance.coordinate_row


def removeEqual(coord_row, coordinate_row_instance):
    for i in range(len(coord_row)):
        if '=' in coord_row[i]:
            coordinate_row_instance.add(coord_row[i].split('='))
        else:
            coordinate_row_instance.add(coord_row[i])


def flatten(lst):
    return sum(([x] if not isinstance(x, list) else flatten(x)for x in lst), [])


f = file_input()
content = f.splitlines()
coords = [i.split() for i in content]
print coords
cr = CoordinateRow()
addAll(coords[0], cr)
cr2 = CoordinateRow()
print cr.coordinate_row
removeEqual(coords[0], cr2)
print cr2.coordinate_row
print flatten(cr2.coordinate_row)


