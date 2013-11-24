'''Assignment: Weave1
   Created on 24-11-2013
   @author: Daan Helsloot (dht340) '''
import sys

from RowWeaver import RowWeaver


def readRows(row_one, row_two):
    result = RowWeaver()
    for i in range(0, min(len(row_one), len(row_two))):
        result.add(row_one[i], row_two[i])
    return result

row_one = sys.stdin.readline().split()
row_two = sys.stdin.readline().split()

row = readRows(row_one, row_two)
print row

# for i in range(0, min(len(row_one), len(row_two))):
#     print row_one[i] + " " + row_two[i],
