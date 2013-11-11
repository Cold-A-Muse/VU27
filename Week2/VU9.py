import sys
__author__ = 'Helsloot'

array = raw_input("Select at least 3 numbers to calculate the second smallest seperated by commas: ")

splitted = array.strip(" ").split(",")
numbers = [int(x) for x in splitted]
min_value = sys.maxint


for i in numbers:
    if i < min_value:
        second_min = min_value
        min_value = i
    elif i < second_min:
        second_min = i
        print("Second smallest is: %d" % i)
