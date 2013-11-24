'''Assignment: Weave2
   Created on 24-11-2013
   @author: Daan Helsloot (dht340) '''
import sys

from NumberRow import NumberRow


def readRows(row_one, row_two):
    result = NumberRow()
    for i in range(0, min(len(row_one), len(row_two))):
        result.weave(row_one[i])
        result.weave(row_two[i])
    return result

row_one = sys.stdin.readline().split()
row_two = sys.stdin.readline().split()
row_three = sys.stdin.readline().split()

row = readRows(row_one, row_two)
weaved = readRows(row, row_three)
print weaved

# for i in range(0, min(len(row_one), len(row_two))):
#     print row_one[i] + " " + row_two[i],
